from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from typing import List, Optional
from pydantic import BaseModel
import config
import numpy as np
from sklearn.manifold import TSNE

client = MongoClient(host=config.MONGODB_HOST, port=config.MONGODB_PORT)

client.server_info()

db = client[config.MONGODB_DATABASE]

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
    if label:
        return categoriesCollection.find_one({}, label)
    else:
        return categoriesCollection.find_one({})

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
    output_args = ["title", "artistName", "description", "image", "styles", "galleries"]
    data = {'data': [paintingsCollection.find_one({'_id': _id}, output_args) for _id in ids]}
    return data

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
def paintingPosition(artistName: Optional[List[str]] = Query(None), galleries: Optional[List[str]] = Query(None),
                     genres: Optional[List[str]] = Query(None), media: Optional[List[str]] = Query(None),
                     period: Optional[List[str]] = Query(None), styles: Optional[List[str]] = Query(None),
                     metric: str = None):

    mongo_filter = {}
    if artistName is not None:
        mongo_filter['artistName'] = {"$in": artistName}
    if galleries is not None:
        mongo_filter['galleries'] = {"$in": galleries}
    if genres is not None:
        mongo_filter['genres'] = {"$in": genres}
    if media is not None:
        mongo_filter['media'] = {"$in": media}
    if styles is not None:
        mongo_filter['styles'] = {"$in": styles}
    if period is not None:
        mongo_filter['period'] = {"$in": period}

    output_args = ["image", "width", "height", metric]
    paintings = list(paintingsCollection.find(mongo_filter, output_args))

    #If there is only one image, it's in the center.
    positions = np.array([[0, 0]])
    #If there are more image Compute TSNE with always the same seed.
    if len(paintings) > 1:
        encodings = []
        for painting in paintings:
            encodings.append(painting.pop(metric))
        positions = TSNE(n_components=2, random_state=42).fit_transform(np.stack(encodings))

    for count, painting in enumerate(paintings):
        painting["x"] = positions[count, 0]
        painting["y"] = positions[count, 1]

    max_positions = np.max(positions, axis=0)
    min_positions = np.min(positions, axis=0)

    for painting in paintings:
        painting['paintingsId'] = painting.pop('_id')

    response = {
        "data": paintings,
        "bounding_box": {
            "x_max": max_positions[0],
            "x_min": min_positions[0],
            "y_max": max_positions[1],
            "y_min": min_positions[1],
        }

    }
    return response


