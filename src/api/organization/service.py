from fastapi import BackgroundTasks, HTTPException
from pydantic import ValidationError

from utilities.helpers import generate_api_key
from utilities.encryption import SecretCipher

from db_internal.service import sync_db, mongo_client, BaseSyncDBService
from pymongo import ReturnDocument
from fastapi import HTTPException
from .model import (
    OrganizationBase,
    User,
    UsagePricing,
    Permissions,
    ApiKey,
    TrustedOrgResponse,
)


class OrganizationSyncService:
    def __init__(self):
        self.sync_client = sync_db["organizations"]

    def start_session(self):
        return mongo_client.start_session()

    def create_organization(self, email, metadata={}, users=[]):
        already_exists = self.sync_client.find_one({"users.email": email})
        if already_exists:
            raise HTTPException(status_code=400, detail="User email already exists")

        # Create objects
        users = [User(email=email)]
        permissions = Permissions(rate_limit="10/minute")
        usage = UsagePricing()
        index = "ix-" + generate_api_key()
        apiKey = ApiKey(name="default", indexes=[index])

        # Create organization with the given metadata, user, and index
        try:
            org = OrganizationBase(
                metadata=metadata,
                api_keys=[apiKey],
                indexes=[index],
                users=users,
                permissions=permissions,
                usage=usage,
            )
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

        try:
            # Insert the organization object into the database
            self.sync_client.insert_one(org.model_dump(by_alias=True))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        return org

    def get_organization(self, index_id):
        # Retrieve an organization object by its index_id.
        response = self.sync_client.find_one({"indexes": index_id})

        # Return None if no organization is found.
        if not response:
            raise HTTPException(status_code=400, detail="Organization not found")

        return TrustedOrgResponse(**response)

    def update_organization(self, index_id, updated_data):
        # Find the organization by its ID
        filters = {"indexes": index_id}

        return self.sync_client.find_one_and_update(
            filters,
            {"$set": updated_data},
            return_document=ReturnDocument.AFTER,
        )

    def get_by_api_key(self, api_key):
        obj = self.sync_client.find_one({"api_keys.key": api_key})

        # Raise an error if no user is found with the given API key.
        if obj is None:
            raise HTTPException(status_code=400, detail="API key does not exist")

        return obj

    def get_index_ids(self, api_key, index_id=None):
        obj = self.get_by_api_key(api_key)
        if not obj["indexes"]:
            raise HTTPException(status_code=400, detail="No index_ids for user")
        if index_id and index_id in obj["indexes"]:
            return index_id
        elif index_id:
            raise HTTPException(status_code=400, detail="Provided index not found")

        # temp until we can handle multiple index_ids
        return obj["indexes"][0], obj

    def get_by_index_id(self, index_id):
        # Retrieve an organization object by its index_id.
        response = self.sync_client.find_one({"indexes": index_id})

        # Return None if no organization is found.
        if not response:
            raise HTTPException(detail="Organization not found", status_code=400)

        return OrganizationBase(**response)
