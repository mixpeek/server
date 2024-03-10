import httpx
from tika import parser
from io import BytesIO


class FileTextExtractor:
    def __init__(self, file_url=None, file=None):
        self.file_url = file_url
        self.file = file

    async def download_file_to_memory(self):
        if self.file:
            # Read the file into memory
            return BytesIO(self.file.read()), None, 200
        else:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(self.file_url)
                    response.raise_for_status()  # Raises exception for 4XX/5XX responses
                    return BytesIO(response.content), None, 200
            except httpx.HTTPStatusError as e:
                # Catch HTTP errors and return more specific error information
                return (
                    None,
                    f"HTTP Error while downloading the file: {e}",
                    e.response.status_code,
                )
            except httpx.RequestError as e:
                # Catch any other httpx exceptions
                return None, f"Error downloading the file: {e}", 500
            except Exception as e:
                # Catch all other exceptions
                return None, f"Unexpected error downloading the file: {e}", 500

    async def extract_text(self):
        file_stream, error_message, status_code = await self.download_file_to_memory()
        if file_stream:
            try:
                # Extract text and metadata using Tika directly from the bytes buffer
                # Use getvalue() for async compatibility
                parsed = parser.from_buffer(file_stream.getvalue())
                text = parsed.get("content", "")
                metadata = parsed.get("metadata", {})
                if text:
                    return {
                        "status": "ok",
                        "message": "File text extraction was successful.",
                        "data": {
                            "text": text.strip(),  # Strip to remove leading/trailing whitespace
                            "metadata": metadata,
                        },
                    }, 200
                else:
                    return {
                        "status": "error",
                        "message": "File downloaded but contains no text or could not be parsed.",
                        "data": None,
                    }, 400
            except Exception as e:
                # Handle potential errors during parsing
                return {
                    "status": "error",
                    "message": f"Error parsing the file content: {e}",
                    "data": None,
                }, 500
        else:
            return {
                "status": "error",
                "message": error_message or "Unknown error occurred.",
                "data": None,
            }, status_code
