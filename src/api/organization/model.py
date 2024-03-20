from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Union

from utilities.helpers import generate_api_key
from utilities.encryption import SecretCipher


# Enums
class PricingTier(str, Enum):
    free = "free"
    deluxe = "deluxe"
    premium = "premium"
    startup = "startup"
    enterprise = "enterprise"


class ConnectionType(str, Enum):
    mongodb = "mongodb"
    postgresql = "postgresql"


# Base Schemas
class Permissions(BaseModel):
    rate_limit: str = Field(default="10/minute")  # requests per minute


class UsagePricing(BaseModel):
    credits: int = Field(default=1000)
    pricing_tier: PricingTier = Field(default=PricingTier.free)


class Secret(BaseModel):
    name: Optional[str] = None
    value: bytes

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        cipher = SecretCipher()
        self._value = cipher.encrypt_string(new_value)


class ApiKeyScope(BaseModel):
    user_ids: Optional[List[str]] = None


class ApiKey(BaseModel):
    name: str
    key: str = Field(default_factory=lambda: "sk-" + generate_api_key())
    scope: ApiKeyScope = Field(default_factory=ApiKeyScope)
    indexes: List[str] = Field(default_factory=list)


class Connection(BaseModel):
    type: ConnectionType
    host: str
    port: int = None
    database: str
    username: str
    password: Secret = None
    extra_params: Optional[dict] = (
        None  # For any additional parameters specific to database
    )

    # Validate the port based on the type of database
    @validator("port", always=True)
    def set_default_port(cls, v, values):
        if "type" in values:
            if values["type"] == ConnectionType.mongodb and v is None:
                return 27017
            elif values["type"] == ConnectionType.postgresql and v is None:
                return 5432
        return v

    # Example of how you might validate extra parameters for a specific database type, if necessary
    @validator("extra_params", always=True)
    def validate_extra_params(cls, v, values):
        if "type" in values:
            if values["type"] == ConnectionType.mongodb:
                # MongoDB specific validation can go here
                pass
        return v


# User and Organization Models
class User(BaseModel):
    email: EmailStr
    creation_date: datetime = Field(default_factory=datetime.now)
    metadata: dict = Field(default_factory=dict)
    scope: str = Field(default="organization")


class OrganizationBase(BaseModel):
    org_id: str = Field(default_factory=lambda: "org-" + generate_api_key())
    indexes: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
    creation_date: datetime = Field(default_factory=datetime.now)
    secrets: List[Secret] = Field(default_factory=list)
    api_keys: List[ApiKey] = Field(default_factory=list)
    users: List[User] = Field(default_factory=list)
    permissions: Permissions
    usage: UsagePricing
    connections: List[Connection] = Field(default_factory=list)


# Trusted Response Models
class TrustedUserResponse(BaseModel):
    email: EmailStr
    creation_date: datetime
    metadata: dict
    scope: str


class TrustedOrgResponse(BaseModel):
    org_id: str
    indexes: List[str]
    metadata: dict
    creation_date: datetime
    users: List[TrustedUserResponse]
    permissions: Permissions
    usage: UsagePricing
    api_keys: List[ApiKey] = Field(default_factory=list)
    # connections: List[Connection] = Field(default_factory=list)


# Request Models
class CreateOrgRequest(BaseModel):
    email: EmailStr
    org_metadata: Optional[dict] = {}
    user_metadata: Optional[dict] = {}


class SecretRequest(BaseModel):
    name: str
    value: str


class OrganizationUpdateRequest(BaseModel):
    metadata: Optional[dict] = None
    secrets: Optional[List[Secret]] = None
    api_keys: Optional[List[ApiKey]] = None
    users: Optional[List[User]] = None
    permissions: Optional[Permissions] = None
    # usage: Optional[UsagePricing] = None
    connections: Optional[List[Connection]] = None
