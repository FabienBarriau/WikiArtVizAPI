from fastapi import FastAPI, Query, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from src.ouput_schema import PaintingsDetails, PaintingsPositionSchema
from src.database import Database, Metric, get_db_config
from src.distance import get_distance_between_encoding_and_encoding_list
from src.recommandation import get_recommendations_by_distance
from src.position import get_bounding_box, get_2d_projected_positions
from src.utils import convert_bytes_to_img
from src.encodings import create_encoding_dict

db_config = get_db_config()
database = Database(
    database=db_config.get('DATABASE'),
    host=db_config.get('DATABASE_HOST'),
    port=db_config.get('DATABASE_PORT'),
    username=db_config.get('DATABASE_USERNAME'),
    password=db_config.get('DATABASE_PASSWORD')
)
database.connect()
ENCODINGS_DICT = create_encoding_dict()

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

    encodings_not_formatted = database.get_arts_info(ids, [metric.value])
    encodings = [encoding_not_formated[metric.value] for encoding_not_formated in encodings_not_formatted]
    positions = get_2d_projected_positions(encodings)

    paintings = database.get_arts_info(ids, ["image", "width", "height"])

    for count, painting in enumerate(paintings):
        painting["x"] = positions[count, 0]
        painting["y"] = positions[count, 1]
        painting['paintingsId'] = painting.pop('_id')

    response = {
        "data": paintings,
        "bounding_box": get_bounding_box(positions)
    }
    return response


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

    encodings_not_formatted = database.get_arts_info(ids, [metric.value])
    encodings = [encoding_not_formated[metric.value] for encoding_not_formated in encodings_not_formatted]
    positions = get_2d_projected_positions(encodings)

    paintings = database.get_arts_info(ids, ["image", "width", "height"])

    for count, painting in enumerate(paintings):
        painting["x"] = positions[count, 0]
        painting["y"] = positions[count, 1]
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
    paintings_list = database.get_arts_info(art_ids, infos=["title", "artistName", "description", "image", "styles", "galleries"])
    for painting in paintings_list:
        painting['paintingId'] = painting.pop('_id')
    return {'data': paintings_list}


@app.post('/paintingRecommendation')
def paintings_recommandations_for_user_picture(file: bytes = File(...), nbr: int = Form(...), metric: Metric = Form(...), radius: float = Form(None)):
    img = convert_bytes_to_img(file)
    if img == -1:
        raise HTTPException(status_code=422, detail=f"Failed to load file as an image")
    user_encoding = ENCODINGS_DICT[metric.name].compute_for_one(img)
    db_encodings = database.get_arts_info_for_all([metric.value])
    distance_dict = get_distance_between_encoding_and_encoding_list(user_encoding, db_encodings, metric.value)
    art_ids = get_recommendations_by_distance(distance_dict, nbr, radius)
    paintings_list = database.get_arts_info(art_ids, infos=["title", "artistName", "description", "image", "styles",
                                                            "galleries"])
    for painting in paintings_list:
        painting['paintingId'] = painting.pop('_id')
    return {'data': paintings_list}

