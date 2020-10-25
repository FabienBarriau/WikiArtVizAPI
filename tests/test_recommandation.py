from src.recommandation import get_recommandations
from src.utils import sorted_random_sample
from unittest.mock import patch
import pytest


class TestRecommandation:

    @pytest.fixture()
    def minimal_distance_response_for_art_id(self):
        data = {
            "The Potato eaters": 1,
            "Sower with Setting Sun": 2
        }
        return data

    @pytest.fixture()
    def simple_distance_response_for_art_id(self):
        data = {
            "Wheatfield with Crows": 0.5,
            "Paul Gauguin's Armchair": 0.8,
            "The Potato eaters": 1,
            "Sower with Setting Sun": 2
        }
        return data

    def test_null_nbr(self, mocker, minimal_distance_response_for_art_id):
        mocker.patch(
            'src.recommandation.get_distance_for_art',
            return_value=minimal_distance_response_for_art_id
        )
        assert get_recommandations(art_id="Starry night", nbr=0) == []

    def test_nbr_1_no_radius(self, mocker, minimal_distance_response_for_art_id):
        mocker.patch(
            'src.recommandation.get_distance_for_art',
            return_value=minimal_distance_response_for_art_id
        )
        assert get_recommandations(art_id="Starry night", nbr=1) == ["The Potato eaters"]

    def test_nbr_2_no_radius(self, mocker, minimal_distance_response_for_art_id):
        mocker.patch(
            'src.recommandation.get_distance_for_art',
            return_value=minimal_distance_response_for_art_id
        )
        assert get_recommandations(art_id="Starry night", nbr=2) == ["The Potato eaters", "Sower with Setting Sun"]

    def test_not_null_nbr_null_radius(self, mocker, minimal_distance_response_for_art_id):
        mocker.patch(
            'src.recommandation.get_distance_for_art',
            return_value=minimal_distance_response_for_art_id
        )
        assert get_recommandations(art_id="Starry night", nbr=1, radius=0) == []

    def test_not_enough_art_in_radius(self, mocker, minimal_distance_response_for_art_id):
        mocker.patch(
            'src.recommandation.get_distance_for_art',
            return_value=minimal_distance_response_for_art_id
        )
        assert get_recommandations(art_id="Starry night", nbr=2, radius=1) == ["The Potato eaters"]

    def test_too_much_art_in_radius_1(self, mocker, simple_distance_response_for_art_id):
        mocker.patch(
            'src.recommandation.get_distance_for_art',
            return_value=simple_distance_response_for_art_id
        )
        mocker.patch(
            'src.utils.sorted_random_sample',
            return_value=[[0, 2]]
        )
        assert get_recommandations(art_id="Starry night", nbr=2, radius=1) == \
               ["Wheatfield with Crows", "The Potato eaters"]

    def test_too_much_art_in_radius_2(self, mocker, simple_distance_response_for_art_id):
        mocker.patch(
            'src.recommandation.get_distance_for_art',
            return_value=simple_distance_response_for_art_id
        )
        mocker.patch(
            'src.utils.sorted_random_sample',
            return_value=[[0, 1]]
        )
        assert get_recommandations(art_id="Starry night", nbr=2, radius=1) ==\
               ["Wheatfield with Crows", "Paul Gauguin's Armchair"]

    def test_too_much_art_in_radius_3(self, mocker, simple_distance_response_for_art_id):
        mocker.patch(
            'src.recommandation.get_distance_for_art',
            return_value=simple_distance_response_for_art_id
        )
        mocker.patch(
            'src.utils.sorted_random_sample',
            return_value=[[1, 2]]
        )
        assert get_recommandations(art_id="Starry night", nbr=2, radius=1) == \
               ["Paul Gauguin's Armchair", "The Potato eaters"]