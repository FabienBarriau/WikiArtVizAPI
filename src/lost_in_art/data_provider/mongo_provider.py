from typing import List, Dict, Optional, Any
from lost_in_art.constant import Metric, ArtProperty, FilterableArtProperty, MongoDBCollection
from lost_in_art.annotations import ArtId
from src.lost_in_art.data_provider.data_provider import DataProvider
from lost_in_art.data_provider.mongo_database import MongoDatabase , get_mongo_database

class MongoProvider(DataProvider):

    def __init__(self, mongo_database: MongoDatabase):
        self.database = mongo_database
        self.art_database = self.client[self.database]

    def get_random_arts_ids(self, nbr: int) -> List[str]:
        ids_dict = list(self.art_database[MongoDBCollection.ART].aggregate([{'$sample': {'size': nbr}}]))
        return [id_dict["_id"] for id_dict in ids_dict]

    def get_distance_for_art(self, art_id: ArtId, metric: Metric) -> Dict[ArtId, float]:
        return self.art_database[MongoDBCollection.DISTANCE].find_one({'_id': art_id}, [metric.value])[metric.value]

    def get_arts_ids(self, filters: Optional[Dict[FilterableArtProperty, Any]] = None) -> List[ArtId]:
        if filters is None:
            return []
        else:
            mongo_filter = {}
            for key, value in filters.items():
                if value is not None:
                    mongo_filter[key] = {"$in": value}
            ids_dict = list(self.art_database[MongoDBCollection.ART].find(mongo_filter, []))
            return [id_dict["_id"] for id_dict in ids_dict]

    def get_arts_properties(self, arts_ids: List[ArtId], properties: List[ArtProperty]) -> List[Dict[ArtProperty, Any]]:
        return [self.art_database[MongoDBCollection.ART].find_one({'_id': art_id}, properties) for art_id in arts_ids]

    def get_arts_info_for_all(self, properties: List[ArtProperty]) -> List[Dict[ArtProperty, Any]]:
        return list(self.art_database[MongoDBCollection.ART].find({}, properties))

    def get_categories(self, label: List[str]) -> Dict[str, str]:
        if label:
            return self.art_database[MongoDBCollection.CATEGORY].find_one({}, label)
        else:
            return self.art_database[MongoDBCollection.CATEGORY].find_one({})

def get_mongo_provider():
    yield MongoProvider(get_mongo_database())