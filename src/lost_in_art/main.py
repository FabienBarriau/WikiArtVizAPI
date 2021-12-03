from fastapi import FastAPI, Query, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from lost_in_art.ouput_schema import PaintingsDetails, PaintingsPositionSchema
from lost_in_art.data_provider.mongo_provider import get_mongo_provider
from lost_in_art.distance import get_distance_between_encoding_and_encoding_list
from lost_in_art.recommandation import GetRecommendation
from lost_in_art.position import GetPaintingsPosition
from lost_in_art.utils import convert_bytes_to_img
from lost_in_art.encodings import create_encoding_dict

provider = get_mongo_provider()
get_recommendation = GetRecommendation(provider)
get_painting_position = GetPaintingsPosition(provider)

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


@app.get('/paintingsDetail', response_model=PaintingsDetails)
def paintings_detail(ids: List[str] = Query(None)):
    paintings_list = database.get_arts_info(ids, ["title", "artistName", "description", "image", "styles", "galleries"])
    for painting in paintings_list:
        painting['paintingId'] = painting.pop('_id')
    return {'data': paintings_list}


@app.get('/paintingsPosition/randomSample', response_model=PaintingsPositionSchema)
def paintings_positions_random(nbr: int, metric: Metric):
    ids = database.get_random_arts_ids(nbr)
    return get_painting_position(ids)


@app.get('/paintingsPosition/appliedFilters', response_model=PaintingsPositionSchema)
def paintings_positions(metric: Metric,
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
    return get_painting_position(ids)

@app.get('/paintingRecommendation', response_model=PaintingsDetails)
def paintings_recommendations(art_id: str, nbr: int, metric: Metric, radius: float = None):
    return {'data': get_recommendation.get_recommandations_for_an_image(art_id=art_id, nbr=nbr, metric=metric, radius=radius)}


@app.post('/paintingRecommendation')
def paintings_recommandations_for_user_picture(file: bytes = File(...), nbr: int = Form(...), metric: Metric = Form(...), radius: float = Form(None)):
    img = convert_bytes_to_img(file)
    if img == -1:
        raise HTTPException(status_code=422, detail=f"Failed to load file as an image")
    return {'data': get_recommendation.get_recommandations_for_an_image(img=img, nbr=nbr, metric=metric, radius=radius)}

