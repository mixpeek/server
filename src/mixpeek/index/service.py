from fastapi import HTTPException
import httpx
import json
import asyncio
import uuid


class HTTPClientError(Exception):
    pass


class HTTPClient:
    def __init__(self, base_url, max_retries=3, retry_delay=5):
        self.base_url = base_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def send_request(self, endpoint, payload):
        url = f"{self.base_url}/{endpoint}"
        request_payload = json.dumps(payload)
        for i in range(self.max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(url, data=request_payload)
                    response.raise_for_status()
                    return response.content
            except (httpx.HTTPStatusError, httpx.RequestError) as e:
                if i == self.max_retries - 1:  # If this was the last attempt
                    raise HTTPClientError(
                        f"Request failed after {self.max_retries} attempts: {e}"
                    ) from e
                else:
                    await asyncio.sleep(
                        self.retry_delay
                    )  # Wait before the next attempt


class Worker:
    def __init__(self, service):
        self.service = service

    async def process_chunk(self, chunk):
        content = chunk["content"]
        embedding = await self.service.embed(content)
        await self.service.insert(
            {
                "file_id": content["file_id"],
                "embedding_id": str(uuid.uuid4()),
                "content": content,
                "embedding": embedding.tolist(),
                "file_metadata": {},
            }
        )


class IndexService:
    def __init__(self, connection_object, base_url):
        self.conn = connection_object
        self.http_client = HTTPClient(base_url)

    async def _send_request(self, service, payload):
        try:
            return await self.http_client.send_request(service, payload)
        except HTTPClientError as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def extract(self, file_url):
        payload = {"file_url": file_url}
        return await self._send_request("extract_chunks", payload)

    async def embed(self, corpus):
        payload = {"corpus": corpus}
        return await self._send_request("embed", payload)

    async def insert(self, obj):
        payload = {"obj": obj}
        return await self._send_request("insert", payload)

    async def process(self, file_url, num_workers):
        chunks = await self.extract(file_url)
        queue = asyncio.Queue()

        for chunk in chunks:
            await queue.put(chunk)

        workers = [Worker(self) for _ in range(num_workers)]
        tasks = [
            asyncio.create_task(worker.process_chunk(await queue.get()))
            for worker in workers
        ]

        await queue.join()

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)
