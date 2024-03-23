from openai import OpenAI, NotFoundError
from pydantic import BaseModel, Field, ValidationError
import copy

from config import openai_key
import json
import time

from generate.models.model import GenerationRequest, GenerationResponse
from _utils import generate_uuid, current_time
from _exceptions import (
    JSONSchemaParsingError,
    ModelExecutionError,
    UnsupportedModelVersionError,
    ModelResponseFormatValidationError,
    BadRequestError,
)


client = OpenAI(api_key=openai_key)


class GPT:
    def __init__(self, generation_request: GenerationRequest):
        self.generation_request = generation_request

    def _resolve_references(self, schema, definitions):
        if isinstance(schema, dict):
            if "$ref" in schema:
                ref_path = schema["$ref"].split("/")[-1]
                return self._resolve_references(definitions[ref_path], definitions)
            else:
                for key, value in schema.items():
                    schema[key] = self._resolve_references(value, definitions)
        elif isinstance(schema, list):
            for i, item in enumerate(schema):
                schema[i] = self._resolve_references(item, definitions)
        return schema

    def _simplify_anyof_allof(self, schema):
        if isinstance(schema, dict):
            if "anyOf" in schema:
                return self._simplify_anyof_allof(schema["anyOf"][0])
            elif "allOf" in schema:
                return self._simplify_anyof_allof(schema["allOf"][0])
            else:
                for key, value in schema.items():
                    schema[key] = self._simplify_anyof_allof(value)
        elif isinstance(schema, list):
            for i, item in enumerate(schema):
                schema[i] = self._simplify_anyof_allof(item)
        return schema

    def _transform_schema(self, schema):
        schema_copy = copy.deepcopy(schema)
        definitions = schema_copy.get("$defs", {})
        resolved_schema = self._resolve_references(schema_copy, definitions)
        simplified_schema = self._simplify_anyof_allof(resolved_schema)
        if "$defs" in simplified_schema:
            del simplified_schema["$defs"]
        return simplified_schema

    def _extract_response_format(self):
        if not self.generation_request.response_format:
            return None
        json_schema = self.generation_request.response_format
        transformed_schema = self._transform_schema(json_schema)
        return transformed_schema

    def _extract_settings(self):
        if self.generation_request.settings:
            return {
                k: v
                for k, v in self.generation_request.settings.model_dump().items()
                if v is not None and k != "system_prompt"
            }
        return {}

    def run(self):
        response_object = GenerationResponse(
            generation_id=generate_uuid(),
            created_at=current_time(),
            model=self.generation_request.model,
            metadata=None,
            response={},
            error=None,
            status=500,
            success=False,
        )

        settings = self._extract_settings()
        response_format = self._extract_response_format()

        if self.generation_request.context:
            self.generation_request.messages.append(
                {"role": "user", "content": self.generation_request.context}
            )
        messages = [{"role": "user", "content": self.generation_request.context}]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "function",
                    "description": "",
                    "parameters": response_format,
                },
            }
        ]

        start_time = time.time() * 1000
        try:
            r = client.chat.completions.create(
                model=self.generation_request.model.model,
                messages=messages,
                tools=tools,
                tool_choice="auto",  # auto is default, but we'll be explicit
                **settings,
            )

            gpt_response = r.json()

            print(gpt_response)

            if "error" in gpt_response:
                raise BadRequestError(error=str(gpt_response["error"]))

            message = gpt_response["choices"][0]["message"]
            if "tool_calls" in message:
                combined_response = {}
                for tool_call in message["tool_calls"]:
                    if tool_call["type"] == "function":
                        print(json.dumps(tool_call["function"]["arguments"]))
                        try:
                            tool_call_args = json.loads(
                                tool_call["function"]["arguments"]
                            )
                            for key, value in tool_call_args.items():
                                if key not in combined_response:
                                    combined_response[key] = []
                                # If the value is a list of dictionaries, iterate over the dictionaries
                                if isinstance(value, list) and all(
                                    isinstance(i, dict) for i in value
                                ):
                                    for i in value:
                                        combined_response[key].append(i)
                                else:
                                    combined_response[key].extend(
                                        value if isinstance(value, list) else [value]
                                    )
                        except Exception as e:
                            print(f"Error processing tool call arguments: {e}")
                response_object.response = combined_response
            else:
                response_object.response = message["content"]

            response_object.metadata = {
                "elapsed_time": (time.time() * 1000) - start_time,
                "total_tokens": gpt_response["usage"]["total_tokens"],
            }
            response_object.status = 200
            response_object.success = True

            return response_object

        except NotFoundError as e:
            raise UnsupportedModelVersionError()

        except ValidationError as e:
            raise ModelResponseFormatValidationError(
                error=str(e),
                suggestion="Make the problematic field Optional to allow for null fields.",
            )

        except Exception as e:
            raise ModelExecutionError()
