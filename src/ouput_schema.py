from pydantic import BaseModel
from typing import List, Optional


class PaintingDetail(BaseModel):
    paintingId: str
    title: str
    artistName: str
    image: Optional[str]
    description: Optional[str]
    galleries: Optional[List[str]]
    styles: Optional[List[str]]


class PaintingsDetails(BaseModel):
    data: List[PaintingDetail]


class PaintingSchema(BaseModel):
    paintingsId: str
    image: str
    x: float
    y: float
    width: float
    height: float


class BoundingBoxSchema(BaseModel):
    x_max: float
    x_min: float
    y_max: float
    y_min: float


class PaintingsPositionSchema(BaseModel):
    data: List[PaintingSchema]
    bounding_box: BoundingBoxSchema