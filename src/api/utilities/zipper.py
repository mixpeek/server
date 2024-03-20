import os
import subprocess
import shutil
import venv
import io
import zipfile
import requests

from fastapi import HTTPException

from config import services_url


class CodeZipper:
    @staticmethod
    def zip_code(function_name, code_string):
        # Create a new buffer to hold the zip file
        zip_buffer = io.BytesIO()

        # Create a new zip file in the buffer
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Add the code string as a file to the zip file
            zip_info = zipfile.ZipInfo(f"{function_name}.py")
            zip_info.external_attr = 0o755 << 16  # permissions -rwxr-xr-x
            zip_file.writestr(f"{function_name}.py", code_string)

        zip_buffer.seek(0)
        return zip_buffer


class PackageZipper:
    def __init__(self, data):
        self.data = data

    def call_endpoint(self):
        response = requests.post(f"{services_url}/package", json=self.data)
        return response.json()

    def load_zip_in_memory(self, s3_path):
        response = requests.get(s3_path, stream=True)
        zip_in_memory = io.BytesIO(response.content)
        return zip_in_memory

    def update_code(function_name, old_zip, new_code):
        # Create a new buffer and copy the old zip file to it
        zip_buffer = io.BytesIO()
        zip_buffer.write(old_zip.getvalue())
        zip_buffer.seek(0)

        # Open the new zip file and overwrite the Python function
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
            # Create a ZipInfo object to set the permissions
            zip_info = zipfile.ZipInfo(f"{function_name}.py")
            zip_info.external_attr = 0o755 << 16  # Set permissions to 0o755

            zip_file.writestr(zip_info, new_code)

        zip_buffer.seek(0)
        return zip_buffer

    def get_s3_url(self):
        """This returns: {"bucket": s3_bucket_name, "key": f"{function_name}.zip"}"""
        try:
            return self.call_endpoint()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
