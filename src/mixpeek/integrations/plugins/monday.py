import httpx
import json
from fastapi import HTTPException


class MondayClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }
        self.url = "https://api.monday.com/v2"

    async def _make_request(self, query):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.url, headers=self.headers)
                return response.json(), response.status_code
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def create_webhook(
        self, board_id, webhook_url, event, column_id, column_value
    ):
        query = f"""
            mutation {{
                create_webhook (board_id: {board_id}, url: "{webhook_url}", event: {event}, config: {{ "columnId": "{column_id}", "columnValue": {json.dumps(column_value)} }}) {{
                    id
                    board_id
                }}
            }}
        """
        return await self._make_request(query=json.dumps({"query": query}))


# board_id = 1234567890  # Replace with your actual board ID
# webhook_url = "https://www.webhooks.my-webhook/test/"  # Replace with your actual webhook URL
# event = "change_status_column_value"  # Replace with your actual event
# column_id = "status"  # Replace with your actual column ID
# column_value = {"$any$": True}  # Replace with your actual column value condition
