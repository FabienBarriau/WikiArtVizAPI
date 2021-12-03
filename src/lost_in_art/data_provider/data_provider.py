from typing import List, Dict, Optional, Any
from abc import ABCMeta, abstractmethod
from lost_in_art.constant import Metric, ArtProperty, FilterableArtProperty
from lost_in_art.annotations import ArtId

class DataProvider(ABCMeta):

    @abstractmethod
    def get_random_arts_ids(self, nbr: int) -> List[str]:
        """Get n random art ids.

        Args:
            nbr (int): number of art.

        Returns:
            List[str]: list of ids.
        """

    @abstractmethod
    def get_distance_for_art(self, art_id: ArtId, metric: Metric) -> Dict[ArtId, float]:
        """Get a dict with all distance of the choosen metric between the choosen art_id and all the others arts.

        Args:
            art_id (ArtId): An art id.
            metric (Metric): A distance metric.

        Returns:
            Dict[ArtId, float]: A dict with art id as keys and distance as values.
        """

    @abstractmethod
    def get_arts_ids(self, filters: Optional[Dict[FilterableArtProperty, Any]] = None) -> List[ArtId]:
        """Get all arts ids that match the intersection of all filters.

        Args:
            filters (Optional[Dict[str, str]], optional): [description]. A dict with names of the properties as keys and the values to filter as values.

        Returns:
            List[ArtId]: A list of art ids.
        """

    @abstractmethod
    def get_arts_properties(self, arts_ids: List[ArtId], properties: List[ArtProperty]) -> List[Dict[ArtProperty, Any]]:
        """Get properties for a list of art ids

        Args:
            arts_ids (List[ArtId]): An art id.
            properties (List[ArtProperty]): list of properties

        Returns:
            List[Dict[ArtProperty, Any]]:: A list of dict with properties as keys and values as values
        """

    @abstractmethod
    def get_arts_info_for_all(self, properties: List[ArtProperty]) -> List[Dict[ArtProperty, Any]]:
        """Get properties for all of art ids

        Args:
            properties (List[ArtProperty]): list of properties

        Returns:
            List[Dict[ArtProperty, Any]]:: A list of dict with properties as keys and values as values
        """

    @abstractmethod
    def get_categories(self, label: List[str]) -> Dict[str, str]:
        """Get categories

        Args:
            label (List): A list of labels

        Returns:
            Dict: A dict of categories
        """

