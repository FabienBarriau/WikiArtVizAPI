import math
import numpy as np
from typing import List


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