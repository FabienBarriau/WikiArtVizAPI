from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import numpy as np
from sklearn.manifold import TSNE
from schema import PaintingsPositionSchema, PaintingsDetailsSchema
from flask_cors import CORS
import config as config

app = Flask(__name__)
CORS(app)

if (config.MONGODB_USERNAME is None) & (config.MONGODB_PASSWORD is None):
    client = MongoClient(host=config.MONGODB_HOST, port=config.MONGODB_PORT)
else:
    client = MongoClient(host=config.MONGODB_HOST, port=config.MONGODB_PORT,
                         username=config.MONGODB_USERNAME, password=config.MONGODB_PASSWORD)
client.server_info()

db = client[config.MONGODB_DATABASE]

paintingsCollection = db['paintings']
categoriesCollection = db['categories']

@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome in WikiArt API'

@app.route('/api/v1/categories', methods=['GET'])
@use_args({"labels": fields.DelimitedList(fields.Str())}, location="query")
def categories(args):
    if args:
        return categoriesCollection.find_one({}, args['labels'])
    else:
        return categoriesCollection.find_one({})

paintingsPostionParams = {
    "artistName": fields.List(fields.Str()),
    "galleries": fields.List(fields.Str()),
    "genres": fields.List(fields.Str()),
    "media": fields.List(fields.Str()),
    "period": fields.List(fields.Str()),
    "styles": fields.List(fields.Str()),
    "metric": fields.Str(),
}
@app.route('/api/v1/paintingsPosition', methods=['GET'])
@use_args(paintingsPostionParams, location="query")
def paintingPosition(args):
    mongo_filter = {}
    print(args["metric"])
    for arg in args:
        if arg in ["styles", "galleries", "genres", "media", "period", "artistName"]:
            mongo_filter[arg] = {"$in": args[arg]}
    output_args = ["image", "width", "height", args["metric"]]
    paintings = list(paintingsCollection.find(mongo_filter, output_args))

    positions = [[0, 0]]
    if len(paintings) > 1:
        encodings = []
        for painting in paintings:
            encodings.append(painting.pop(args["metric"]))
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

    return PaintingsPositionSchema().dump(response)

paintingsDetailParams = {
    "ids": fields.List(fields.Str()),
}
@app.route('/api/v1/paintingsDetail', methods=['GET'])
@use_args(paintingsDetailParams, location="query")
def paintingsDetail(args):
    output_args = ["title", "artistName", "description", "image", "styles", "galleries"]
    data = {"data": [paintingsCollection.find_one({'_id': _id}, output_args) for _id in args["ids"]]}
    return PaintingsDetailsSchema().dump(data)


if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.APP_DEBUG)