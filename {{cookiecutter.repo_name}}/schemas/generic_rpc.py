from typing import List, Dict, Any

from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)


class DeleteRequest(BaseModel):
    uuid: int = Field(default_factory=int)


class GetRequest(BaseModel):
    uuid: int = Field(default_factory=int)


class ItemResponse(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)


class ListRequest(BaseModel):
    filters: Dict[str, Any] = Field(default_factory=dict)
    offset: int = Field(default_factory=int)
    limit: int = Field(default_factory=int)
    ordering: List[str] = Field(default_factory=list)


class ListResponse(BaseModel):
    data: List[Dict[str, Any]] = Field(default_factory=list)
    count: int = Field(default_factory=int)


class ResultResponse(BaseModel):
    result: bool = Field(default_factory=bool)


class UpdateRequest(BaseModel):
    uuid: int = Field(default_factory=int)
    data: Dict[str, Any] = Field(default_factory=dict)
