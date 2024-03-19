from fastapi import HTTPException
from db_internal.service import BaseAsyncDBService


from config import listener_url



class ListenerAsyncService(BaseAsyncDBService):
    def __init__(self, index_id):
        super().__init__("listeners", index_id)
        self.listener_url = listener_url
