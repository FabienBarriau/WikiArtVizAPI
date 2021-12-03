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


