from pydantic import BaseModel

ArtId = str

class Painting(BaseModel):
    paintingsId: str
    image: str
    x: float
    y: float
    width: float
    height: float