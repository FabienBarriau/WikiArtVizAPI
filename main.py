from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import numpy as np
from sklearn.manifold import TSNE
from src.database import Database, Metric, get_config
from src.recommandation import get_recommendations_by_distance
from src.position import get_bounding_box

config = get_config()
database = Database(
    database=config.get('DATABASE'),
    host=config.get('DATABASE_HOST'),
    port=config.get('DATABASE_PORT'),
    username=config.get('DATABASE_USERNAME'),
    password=config.get('DATABASE_PASSWORD')
)
database.connect()

db = database.get_db()

paintingsCollection = db['paintings']
categoriesCollection = db['categories']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get('/categories')
def categories(label: Optional[List[str]] = Query(None)):
    return database.get_categories(label)


class PaintingDetail(BaseModel):
    _id: str
    title: str
    artistName: str
    image: Optional[str]
    description: Optional[str]
    galleries: Optional[List[str]]
    styles: Optional[List[str]]


class PaintingsDetails(BaseModel):
    data: List[PaintingDetail]


@app.get('/paintingsDetail', response_model=PaintingsDetails)
def paintingsDetail(ids: List[str] = Query(None)):
    return {'data': database.get_arts_info(ids, ["title", "artistName", "description", "image", "styles", "galleries"])}


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


@app.get('/paintingsPosition', response_model=PaintingsPositionSchema)
def paintingPosition(metric: Metric,
                     artistName: Optional[List[str]] = Query(None), galleries: Optional[List[str]] = Query(None),
                     genres: Optional[List[str]] = Query(None), media: Optional[List[str]] = Query(None),
                     period: Optional[List[str]] = Query(None), styles: Optional[List[str]] = Query(None)):

    filter = {
        "artistName": artistName,
        "galleries": galleries,
        "genres": genres,
        "media": media,
        "period": period,
        "styles": styles
    }
    ids = database.get_arts_ids(filter)
    paintings = database.get_arts_info(ids, ["image", "width", "height", metric.value])

    #If there is only one image, it's in the center.
    positions = np.array([[0, 0]])
    #If there are more image Compute TSNE with always the same seed.
    if len(paintings) > 1:
        encodings = []
        for painting in paintings:
            encodings.append(painting.pop(metric.value))
        positions = TSNE(n_components=2, random_state=42).fit_transform(np.stack(encodings))

    for count, painting in enumerate(paintings):
        painting["x"] = positions[count, 0]
        painting["y"] = positions[count, 1]

    for painting in paintings:
        painting['paintingsId'] = painting.pop('_id')

    response = {
        "data": paintings,
        "bounding_box": get_bounding_box(positions)
    }
    return response


@app.get('/paintingRecommendation', response_model=PaintingsDetails)
def paintings_recommendations(art_id: str, nbr: int, metric: Metric, radius: float = None):
    distance_dict = database.get_distance_for_art(art_id, metric)
    art_ids = get_recommendations_by_distance(distance_dict, nbr, radius)
    return {'data': database.get_arts_info(art_ids, infos=["title", "artistName", "description", "image", "styles", "galleries"])}


