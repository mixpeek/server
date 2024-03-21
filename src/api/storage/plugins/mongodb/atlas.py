import httpx
import json


class AtlasClient:
    def __init__(self, cluster_name, group_id, public_key, private_key):
        self.cluster_name = cluster_name
        self.group_id = group_id
        self.public_key = public_key
        self.private_key = private_key
        self.headers = {"Content-Type": "application/vnd.atlas.2023-01-01+json"}
        self.index = Index(self)
        self.trigger = Trigger(self)

    async def _post_request(self, url, data):
        async with httpx.AsyncClient() as client:
            r = await client.post(
                url,
                headers=self.headers,
                data=json.dumps(data),
                auth=(self.public_key, self.private_key),
            )
        return r.text


class Index:
    def __init__(self, client):
        self.client = client

    async def create(self):
        url = f"https://cloud.mongodb.com/api/atlas/v2/groups/{self.client.group_id}/clusters/{self.client.cluster_name}/fts/indexes?pretty=true"
        payload = {
            "collectionName": "string",
            "database": "string",
            "name": "string",
            "type": "vectorSearch",
            "fields": [{"property1": {}, "property2": {}}],
        }

    async def list(self):
        pass

    async def delete(self):
        pass


class Trigger:
    def __init__(self, client):
        self.client = client

    async def create(
        self, trigger_name, trigger_type, function_name, event_subscription
    ):
        url = "https://services.cloud.mongodb.com/api/admin/v3.0/groups/{groupId}/apps/{appId}/triggers"
        trigger_payload = {
            "name": "onNewEmployee",
            "type": "DATABASE",
            "function_id": "5eea9ca4ca0e356e2c2a148a",
            "config": {
                "operation_types": ["INSERT", "UPDATE", "REPLACE", "DELETE"],
                "database": "HR",
                "collection": "employees",
                "service_id": "5adeb649b8b998486770ae7c",
                "match": {},
                "project": {},
                "full_document": True,
            },
        }
        response_text = await self.client._post_request(url=url, data=trigger_payload)
        return response_text

    async def list(self):
        pass

    async def delete(self):
        pass
