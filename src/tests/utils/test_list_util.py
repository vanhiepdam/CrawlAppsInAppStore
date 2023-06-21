from utils.list import ListUtil


class TestPythonUtil:
    def test_split_array_into_chunks__empty_array(self):
        # Arrange
        array = []
        chunk_size = 10

        # Act
        result = ListUtil.split_array_into_chunks(array, chunk_size)

        # Assert
        assert list(result) == []

    def test_split_array_into_chunks__array_size_less_than_chunk_size(self):
        # Arrange
        array = [1, 2, 3]
        chunk_size = 10

        # Act
        result = ListUtil.split_array_into_chunks(array, chunk_size)

        # Assert
        assert list(result) == [[1, 2, 3]]

    def test_split_array_into_chunks__array_size_equal_to_chunk_size(self):
        # Arrange
        array = [1, 2, 3]
        chunk_size = 3

        # Act
        result = ListUtil.split_array_into_chunks(array, chunk_size)

        # Assert
        assert list(result) == [[1, 2, 3]]

    def test_split_array_into_chunks__array_size_greater_than_chunk_size(self):
        # Arrange
        array = [1, 2, 3, 4, 5]
        chunk_size = 3

        # Act
        result = ListUtil.split_array_into_chunks(array, chunk_size)

        # Assert
        assert list(result) == [[1, 2, 3], [4, 5]]
