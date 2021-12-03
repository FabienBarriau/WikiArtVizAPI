from typing import List
from lost_in_art.constant import Metric, ArtProperty
from lost_in_art.utils import sorted_random_sample
from lost_in_art.annotations import ArtId
from lost_in_art.data_provider.data_provider import DataProvider
from lost_in_art.encodings import create_encoding_dict
from lost_in_art.distance import get_distance_between_encoding_and_encoding_list

class GetRecommendation:

    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider
        self.encoding_dict = create_encoding_dict()

    def get_recommendations_for_art_id(self, art_id: str, nbr: int, metric: Metric, radius: float) -> List[ArtId]:
        distance_dict = self.data_provider.get_distance_for_art(art_id, metric)
        art_ids = self._get_recommendations_by_distance(distance_dict, nbr, radius)
        return self._add_info_to_arts_ids(art_ids)


    def get_recommandations_for_an_image(self, img, nbr: int, metric: Metric, radius: float):
        user_encoding = self.encoding_dict[metric.name].compute_for_one(img)
        db_encodings = self.data_provider.get_arts_info_for_all([metric.value])
        distance_dict = get_distance_between_encoding_and_encoding_list(user_encoding, db_encodings, metric.value)
        art_ids = self._get_recommendations_by_distance(distance_dict, nbr, radius)
        return self._add_info_to_arts_ids(art_ids)

    def _get_recommendations_by_distance(distance_dict: dict, nbr: int, radius: float = None) -> list:
        if (nbr == 0) | (radius == 0):
            return []
        else:
            if radius is None:
                distance_listed_tuples = [(v, k) for k, v in distance_dict.items()]
                art_id_sort_by_distance_value = [x for _, x in sorted(distance_listed_tuples)]
                return art_id_sort_by_distance_value[0:nbr]
            else:
                distance_listed_tuples_filtered = [(v, k) for k, v in distance_dict.items() if v <= radius]
                art_id_sort_by_distance_value_filtered = [x for _, x in sorted(distance_listed_tuples_filtered)]
                n = len(art_id_sort_by_distance_value_filtered)
                if n <= nbr:
                    return art_id_sort_by_distance_value_filtered
                else:
                    art_id_sort_by_distance_value_filtered_randomly_sample =\
                        [art_id_sort_by_distance_value_filtered[i] for i in sorted_random_sample(n, nbr)]
                    return art_id_sort_by_distance_value_filtered_randomly_sample

    def _add_info_to_arts_ids(self, art_ids):
        props = [
            ArtProperty.TITLE,
            ArtProperty.ARTIST,
            ArtProperty.DESCRIPTION,
            ArtProperty.IMAGE_LINK,
            ArtProperty.STYLES,
            ArtProperty.GALLERIES
        ]
        paintings_list = self.data_provider.get_arts_properties(art_ids, properties=props)
        for painting in paintings_list:
            painting['paintingId'] = painting.pop('_id')
        return paintings_list
