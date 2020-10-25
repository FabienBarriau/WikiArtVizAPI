import numpy as np
from src.utils import sorted_random_sample

def get_distance_for_art(art_id: str) -> dict:
    return {'e': 4, 'r': 2}

def get_recommandations(art_id: str, nbr: int, radius: float=None):
    if (nbr == 0) | (radius == 0):
        return []
    else:
        distance_dict = get_distance_for_art(art_id)
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

