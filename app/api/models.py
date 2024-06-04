from enum import Enum
from typing import Dict, Optional
import uuid
from pydantic import BaseModel


class StatesEnum(str, Enum):
    sp = "sp"
    rj = "rj"
    ba = "ba"
    mg = "mg"


class ItemTypesEnum(str, Enum):
    plastic_box = "plastic_box"
    can = "can"
    plastic_bottle = "plastic_bottle"
    glass_bottle = "glass_bottle"


class StateBase(BaseModel):
    name: str
    shortname: str


class CompanyBase(BaseModel):
    shortname: str
    name: str
    segment: str


class ItemPostRequest(BaseModel):
    token: uuid.UUID
    item_type: ItemTypesEnum
    state: StatesEnum


class ItemPostResponse(BaseModel):
    token: uuid.UUID
    item_type: str
    region: StateBase
    company: CompanyBase


class TotalStatistics(BaseModel):
    total: int
    raw: int
    recycled: int
    recycled_percentage: float


class StatisticsPerItemType(BaseModel):
    type: ItemTypesEnum
    total: int
    raw: int
    recycled: int
    recycled_percentage: float
    

class CompanyStatisticsObject(BaseModel):
    total: TotalStatistics
    item_types: list[StatisticsPerItemType]


class CompanyStatisticsPerStateObject(BaseModel):
    state: Optional[TotalStatistics] = None
    item_types: list[StatisticsPerItemType]


class CompanyStatisticsResponse(CompanyBase):
    shortname: str
    name: str
    segment: str
    statistics: CompanyStatisticsObject


class CompanyStatisticsPerStateResponse(CompanyBase):
    shortname: str
    name: str
    segment: str
    statistics: CompanyStatisticsPerStateObject