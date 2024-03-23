from fastapi import HTTPException
from db.service import BaseAsyncDBService

from .connectors.mongodb import MongoDBChangeHandler

from organization.service import OrganizationSyncService


class PipelineAsyncService(BaseAsyncDBService):
    def __init__(self, index_id):
        super().__init__("pipelines", index_id)
        self.connection = None
        self.source = None
        self.destination = None
        self.change_handler = None

        """
            1. check if the connection exists in the organization
            2. decrypt the connection information
            3. create a connection to the source
            4. create a connection to the destination
            5. create a change handler
            6. process the change
            7. return the response and insert it into the db
        """

    async def check_connection(self, organization):
        # Check if the connection exists in the organization
        pass

    async def decrypt_connection_info(self, connection_info):
        # Decrypt the connection information
        pass

    async def create_source_connection(self, decrypted_info):
        # Create a connection to the source
        pass

    async def create_destination_connection(self, decrypted_info):
        # Create a connection to the destination
        pass

    async def create_change_handler(self):
        # Create a change handler
        pass

    async def process_change(self, change):
        # Process the change
        pass

    async def insert_into_db(self, response):
        # Insert the response into the db
        pass

    async def process_payload(self, payload):
        organization = OrganizationSyncService().get_by_index_id(self.index_id)
        connection_info = payload.get("connection_info")

        change = payload.get("change")

        await self.check_connection(organization)
        decrypted_info = await self.decrypt_connection_info(connection_info)
        self.source = await self.create_source_connection(decrypted_info)
        self.destination = await self.create_destination_connection(decrypted_info)
        self.change_handler = await self.create_change_handler()
        response = await self.process_change(change)
        await self.insert_into_db(response)

        return response
