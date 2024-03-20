from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from utilities.helpers import unique_name
from utilities.encryption import SecretCipher


class ListenerStatus(BaseModel):
    ACTIVE: bool = False
    PROCESSING: int = 0
    COMPLETED: int = 0
    ERROR: int = 0


# class ConnectionType(str, Enum):
#     mongodb = "mongodb"
#     postgresql = "postgresql"


class ConnectionInformation(BaseModel):
    db: str
    username: str
    password: bytes
    host: str
    port: int

    @property
    def password(self):
        return self._value

    @password.setter
    def password(self, new_value):
        cipher = SecretCipher()
        self._value = cipher.encrypt_string(new_value)


class ListenerSchema(BaseModel):
    index_id: str
    created_at: datetime
    provider_id: str
    code_as_string: str
    listener_name: str
    metadata: dict
    # settings: ListenerSettings
    status: ListenerStatus


class ProviderInformation(BaseModel):
    webhook_url: str
    metadata: Optional[dict] = {}


class ListenerCreateRequest(BaseModel):
    provider_id: str
    provider_information: ProviderInformation
    code_as_string: str
    listener_name: Optional[str] = Field(default_factory=unique_name)
    metadata: Optional[dict] = {}
    # settings: Optional[ListenerSettings] = {}
