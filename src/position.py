import numpy as np


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