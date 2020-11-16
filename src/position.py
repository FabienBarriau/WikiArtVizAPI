import numpy as np
from typing import List
from sklearn.manifold import TSNE


def get_bounding_box(positions: np.array) -> dict:
    max_positions = np.max(positions, axis=0)
    min_positions = np.min(positions, axis=0)
    bounding_box = {
        "x_max": max_positions[0],
        "x_min": min_positions[0],
        "y_max": max_positions[1],
        "y_min": min_positions[1],
    }
    return bounding_box


def get_2d_projected_positions(encodings: List[List[float]]) -> np.array:
    # If there is only one image, it's in the center.
    if len(encodings) <= 1:
        return np.array([[0, 0]])
    # If there are more image compute TSNE with always the same seed.
    else:
        return TSNE(n_components=2, random_state=42).fit_transform(np.stack(encodings))
