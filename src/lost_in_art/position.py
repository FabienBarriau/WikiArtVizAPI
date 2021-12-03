import numpy as np
from typing import List
from sklearn.manifold import TSNE
from src.lost_in_art.annotations import ArtId, Painting
from src.lost_in_art.constant import ArtProperty
from src.lost_in_art.data_provider.data_provider import DataProvider
from src.lost_in_art.encodings import Metric
from pydantic import BaseModel

class BoundingBox(BaseModel):
    x_max: float
    x_min: float
    y_max: float
    y_min: float


class PaintingsPosition(BaseModel):
    data: List[Painting]
    bounding_box: BoundingBox

class GetPaintingsPosition:

    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider

    def get_positions_for_arts_ids(self, art_ids: ArtId, metric: Metric) -> PaintingsPosition:
        encodings_not_formatted = self.data_provider.get_arts_properties(art_ids, [metric.value])
        encodings = [encoding_not_formated[metric.value] for encoding_not_formated in encodings_not_formatted]
        positions = self._get_2d_projected_positions(encodings)
        paintings = self.data_provider.get_arts_properties(art_ids, [ArtProperty.IMAGE_LINK, ArtProperty.WIDTH, ArtProperty.HEIGHT])
        for count, painting in enumerate(paintings):
            painting["x"] = positions[count, 0]
            painting["y"] = positions[count, 1]
            painting['paintingsId'] = painting.pop('_id')

        return PaintingsPosition(
            data=[Painting.parse_obj(painting) for painting in paintings],
            bounding_box=self._get_bounding_box(positions)
        )

    def _get_bounding_box(positions: np.array) -> BoundingBox:
        max_positions = np.max(positions, axis=0)
        min_positions = np.min(positions, axis=0)
        return BoundingBox(
            x_max=max_positions[0],
            x_min=min_positions[0],
            y_max=max_positions[1],
            y_min=min_positions[1],
        )

    def _get_2d_projected_positions(encodings: List[List[float]]) -> np.array:
        # If there is only one image, it's in the center.
        if len(encodings) <= 1:
            return np.array([[0, 0]])
        # If there are more image compute TSNE with always the same seed.
        else:
            return TSNE(n_components=2, random_state=42).fit_transform(np.stack(encodings))
