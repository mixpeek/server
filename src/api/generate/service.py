from _exceptions import (
    UnsupportedModelProviderError,
    UnsupportedModelVersionError,
    JSONSchemaParsingError,
    ModelExecutionError,
    ModelResponseFormatValidationError,
    BadRequestError,
    NotFoundError,
    InternalServerError,
)

from .plugins.openai import GPT
from .model import GenerationRequest, GenerationResponse


# Assuming GPT and other model classes have a common run method
# and can be directly instantiated and called without needing an interface.
class ModelHandler:
    @staticmethod
    def model_factory(provider, *args, **kwargs):
        if provider.lower() == "gpt":
            return GPT(*args, **kwargs)
        # TODO: Add other model types like LLaMA, etc
        else:
            raise UnsupportedModelProviderError(
                f"Unsupported model provider: {provider}"
            )


async def generate_orchestrator(request: GenerationRequest) -> GenerationResponse:
    try:
        model_instance = ModelHandler.model_factory(
            request.model.provider,
            request,
        )
        return model_instance.run()

    except UnsupportedModelProviderError as e:
        raise BadRequestError(error="Unsupported model provider.")

    except UnsupportedModelVersionError as e:
        raise NotFoundError(error="Unsupported model version.")

    except JSONSchemaParsingError as e:
        raise BadRequestError(
            error="JSON schema parsing error. Please make sure you provided a valid json schema."
        )

    except ModelExecutionError as e:
        raise InternalServerError(
            error="Something went wrong when calling the model. Please try again."
        )

    except ModelResponseFormatValidationError as e:
        raise BadRequestError(error=str(e))
