import os
import sys
import shutil
import subprocess
import stat
import aioboto3
from config import aws as creds


class PackageManager:
    def __init__(self):
        self.session = aioboto3.Session(
            aws_access_key_id=creds["aws_access_key"],
            aws_secret_access_key=creds["aws_secret_key"],
            region_name=creds["region"],
        )
        self.s3_bucket_name = creds["s3_bucket"]
        self.tmp_dir = "/tmp"

    async def process(self, data):
        try:
            function_name = data["function_name"]
            code = data["code_as_string"]
            requirements = data["requirements"]
            python_version = data.get("python_version", "3.10")

            function_path = self.create_folder(function_name, python_version)
            self.save_code(function_path, function_name, code)
            self.install_requirements(function_path, requirements, python_version)
            zip_path = self.zip_folder(function_path, function_name)
            self.set_permissions(zip_path)
            s3_path = await self.upload_to_s3(zip_path, function_name)

            self.cleanup(function_path, zip_path)
            return {
                "success": True,
                "status": 200,
                "error": None,
                "response": s3_path,
            }, 200
        except Exception as e:
            return {
                "success": False,
                "status": 500,
                "error": f"Error during package creation and upload: {e}",
                "response": None,
            }, 500

    def create_folder(self, function_name, python_version):
        function_path = os.path.join(self.tmp_dir, function_name)
        os.makedirs(function_path, exist_ok=True)
        # Create a virtual environment with the specified Python version
        subprocess.run(
            [python_version, "-m", "venv", os.path.join(function_path, "venv")]
        )
        return function_path

    def save_code(self, function_path, function_name, code):
        with open(os.path.join(function_path, f"{function_name}.py"), "w") as file:
            file.write(code)

    def install_requirements(self, function_path, requirements, python_version):
        req_file = os.path.join(function_path, "requirements.txt")
        with open(req_file, "w") as file:
            file.writelines("\n".join(requirements))
        venv_path = os.path.join(function_path, "venv", "bin", "python")
        subprocess.run(
            [
                venv_path,
                "-m",
                "pip",
                "install",
                "-r",
                req_file,
                "--target",
                function_path,
            ]
        )

    def zip_folder(self, function_path, function_name):
        zip_path = os.path.join(self.tmp_dir, f"{function_name}.zip")
        shutil.make_archive(zip_path.replace(".zip", ""), "zip", function_path)
        return zip_path

    def set_permissions(self, file_path):
        try:
            os.chmod(file_path, 0o755)
        except PermissionError as e:
            print(f"Permission Error: {e}")

    async def upload_to_s3(self, file_path, function_name):
        try:
            async with self.session.client("s3") as client:
                await client.upload_file(
                    file_path, self.s3_bucket_name, f"{function_name}.zip"
                )
            return {"bucket": self.s3_bucket_name, "key": f"{function_name}.zip"}
        except Exception as e:
            print(e)
            return str(e)

    def cleanup(self, function_path, zip_path):
        shutil.rmtree(function_path)
        os.remove(zip_path)
