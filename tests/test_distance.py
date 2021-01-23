from src.distance import get_distance_between_one_and_all, get_distance_between_encoding_and_encoding_list
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

class TestDistanceBetweenEncodingAndListOfEncoding:

    @pytest.fixture
    def encoding(self):
        data = [0, 0]
        return data

    def test_color_encoding_length_1(self, encoding):
        encodings_list = [{'_id': '57727444edc2cb3880cb7bf6', 'color-encoding': [0, 2]}]
        result = get_distance_between_encoding_and_encoding_list(encoding, encodings_list, 'color-encoding')
        expected = {'57727444edc2cb3880cb7bf6': 2}
        assert result == expected
        encodings_list = [{'_id': '57727444edc2cb3880cb7bf6', 'color-encoding': [2, 2]}]
        result = get_distance_between_encoding_and_encoding_list(encoding, encodings_list, 'color-encoding')
        expected = {'57727444edc2cb3880cb7bf6': math.sqrt(8)}
        assert result == expected

    def test_content_encoding_length_1(self, encoding):
        encodings_list = [{'_id': '57727444edc2cb3880cb7bf6', 'encoding': [0, 2]}]
        result = get_distance_between_encoding_and_encoding_list(encoding, encodings_list, 'encoding')
        expected = {'57727444edc2cb3880cb7bf6': 2}
        assert result == expected

    def test_content_encoding_length_2(self, encoding):
        encodings_list = [
            {'_id': '57727444edc2cb3880cb7bf6', 'encoding': [0, 2]},
            {'_id': '5772716cedc2cb3880c19999', 'encoding': [2, 2]}
        ]
        result = get_distance_between_encoding_and_encoding_list(encoding, encodings_list, 'encoding')
        expected = {
            '57727444edc2cb3880cb7bf6': 2,
            '5772716cedc2cb3880c19999': math.sqrt(8)
        }
        assert result == expected

