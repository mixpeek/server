from fastapi import HTTPException
import tempfile
import subprocess
import json
import re


class CodeValidation:
    @staticmethod
    def check_code_security(code, max_code_length=3000, language="python"):
        if len(code) > max_code_length:
            raise HTTPException(
                status_code=400,
                detail=f"Code length exceeds {max_code_length} characters",
            )
        # extensions = {"python": ".py"}
        # with tempfile.NamedTemporaryFile(suffix=".py") as temp:
        #     temp.write(code.encode())
        #     temp.flush()
        #     result = subprocess.run(
        #         ["bandit", temp.name], capture_output=True, text=True
        #     )

        # # Check if bandit found any issues
        # if "No issues identified." in result.stdout:
        #     return True
        # else:
        #     # Parse the issues into a JSON
        #     # Skip the first two lines, which are not issues
        #     issues = result.stdout.split("\n")[2:]
        #     issues_json = [
        #         {"issue": issue} for issue in issues if issue
        #     ]  # Ignore empty lines
        #     return json.dumps(issues_json[1]["issue"])

    @staticmethod
    def check_for_function(code):
        # Check if 'function()' exists and has no parameters
        if "def function(event, context):" not in code:
            raise HTTPException(
                status_code=400,
                detail="Code must contain: def function(event, context):",
            )

        # Check if 'function()' is the only function in the code
        functions = re.findall(r"def \w+\(.*\):", code)
        if len(functions) != 1:
            raise HTTPException(
                status_code=400,
                detail="Code must contain only one function called function.",
            )
        return True

    @staticmethod
    def lint(code):
        with tempfile.NamedTemporaryFile(suffix=".py") as temp:
            temp.write(code.encode())
            temp.flush()
            result = subprocess.run(["ruff", temp.name], capture_output=True, text=True)

        # Return the lint message
        return result.stdout

    @staticmethod
    def convert_to_string(code):
        return repr(code)
