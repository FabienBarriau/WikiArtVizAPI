from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from src.ouput_schema import PaintingsDetails, PaintingsPositionSchema
from src.database import Database, Metric, get_db_config
from src.recommandation import get_recommendations_by_distance
from src.position import get_bounding_box, get_2d_projected_positions

db_config = get_db_config()
database = Database(
    database=db_config.get('DATABASE'),
    host=db_config.get('DATABASE_HOST'),
    port=db_config.get('DATABASE_PORT'),
    username=db_config.get('DATABASE_USERNAME'),
    password=db_config.get('DATABASE_PASSWORD')
)
database.connect()

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
    return {'data': database.get_arts_info(ids, ["title", "artistName", "description", "image", "styles", "galleries"])}


@app.get('/paintingsPosition', response_model=PaintingsPositionSchema)
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
    return {'data': database.get_arts_info(art_ids, infos=["title", "artistName", "description", "image", "styles", "galleries"])}


