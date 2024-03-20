from pydantic import BaseModel


class PackageData(BaseModel):
    function_name: str
    code_as_string: str
    requirements: list[str]
    python_version: str
