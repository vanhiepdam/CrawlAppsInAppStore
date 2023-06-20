from typing import Iterable


class ListUtil:
    @staticmethod
    def split_array_into_chunks(array: list, chunk_size: int) -> Iterable[list]:
        for i in range(0, len(array), chunk_size):
            yield array[i:i + chunk_size]
