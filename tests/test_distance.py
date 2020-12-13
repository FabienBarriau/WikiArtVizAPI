from src.distance import get_distance_between_one_and_all
import pytest
import math


class TestDistanceBetweenOneAndAll:

    @pytest.fixture
    def with_2_color_encoding(self):
        data = [
            {'_id': '57727444edc2cb3880cb7bf6', 'color-encoding': [1, 2]},
            {'_id': '5772716cedc2cb3880c1907f', 'color-encoding': [4, 8]}
        ]
        return data

    @pytest.fixture
    def with_2_content_encoding(self):
        data = [
            {'_id': '57727444edc2cb3880cb7bf6', 'encoding': [1, 2]},
            {'_id': '5772716cedc2cb3880c1907f', 'encoding': [4, 8]}
        ]
        return data

    @pytest.fixture
    def with_3_color_encoding(self):
        data = [
            {'_id': '57727444edc2cb3880cb7bf6', 'color-encoding': [1, 2]},
            {'_id': '5772716cedc2cb3880c1907f', 'color-encoding': [4, 8]},
            {'_id': '5772716cedc2cb3880c19999', 'color-encoding': [0, 0]}
        ]
        return data

    def test_first_with_2_color_encoding(self, with_2_color_encoding):
        result = get_distance_between_one_and_all(0, with_2_color_encoding, 'color-encoding')
        expected_result = {
            '5772716cedc2cb3880c1907f': math.sqrt(45)
        }
        assert result == expected_result

    def test_last_with_2_color_encoding(self, with_2_color_encoding):
        result = get_distance_between_one_and_all(1, with_2_color_encoding, 'color-encoding')
        expected_result = {
            '57727444edc2cb3880cb7bf6': math.sqrt(45)
        }
        assert result == expected_result

    def test_first_with_3_color_encoding(self, with_3_color_encoding):
        result = get_distance_between_one_and_all(0, with_3_color_encoding, 'color-encoding')
        expected_result = {
            '5772716cedc2cb3880c1907f': math.sqrt(45),
            '5772716cedc2cb3880c19999': math.sqrt(5)
        }
        assert result == expected_result

    def test_first_with_2_content_encoding(self, with_2_content_encoding):
        result = get_distance_between_one_and_all(0, with_2_content_encoding, 'encoding')
        expected_result = {
            '5772716cedc2cb3880c1907f': math.sqrt(45)
        }
        assert result == expected_result
