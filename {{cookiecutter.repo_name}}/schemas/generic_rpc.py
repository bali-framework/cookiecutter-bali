from typing import Any, Dict, List

from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)


class DeleteRequest(BaseModel):
    uuid: str = Field(default_factory=str)


class GetRequest(BaseModel):
    uuid: str = Field(default_factory=str)


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
    uuid: str = Field(default_factory=str)
    data: Dict[str, Any] = Field(default_factory=dict)
