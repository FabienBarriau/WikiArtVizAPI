import math
import numpy as np
from typing import List, Dict


def compute_distance_between_one_and_all(encoding: List[float], other_encodings: List[List[float]]) -> np.array:
    return np.linalg.norm(np.array(encoding) - np.array(other_encodings), axis=1)


def get_distance_between_one_and_all(n: int, paintings: list, encoding_name: str) -> dict:
    other_paintings = [paintings[i] for i in range(len(paintings)) if i != n]
    result = {}
    selected_painting_encoding = np.array(paintings[n][encoding_name])
    for count, painting in enumerate(other_paintings):
        other_painting_encoding = np.array(painting[encoding_name])
        result[other_paintings[count]["_id"]] = np.linalg.norm(
            selected_painting_encoding-other_painting_encoding
        )
    return result


def get_distance_between_encoding_and_encoding_list(encoding: List[float], encoding_list: List[Dict], encoding_name: str) -> Dict[str, float]:
    distance_dict = dict()
    for other_encoding in encoding_list:
        distance_dict[other_encoding["_id"]] = np.linalg.norm(np.array(encoding) - np.array(other_encoding[encoding_name]))
    return distance_dict