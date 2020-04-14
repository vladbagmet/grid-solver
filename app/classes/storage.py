import os
import pickle
from typing import Any
from contextlib import suppress

import config
from libs.serializer import Serializer
from app.classes.abstract.storage import AbstractStorage


class Storage(AbstractStorage):
    """
    Implements basic storage functionality.
    Inside real-world applications, storing data into local file system should be replaced with
    key-value storage or DB or cloud-based object storage (like S3).
    """

    def __init__(self):
        self._storage_path = f"{os.getcwd()}/{config.STORAGE_FOLDER_NAME}"
        self._init_storage(self._storage_path)
        self._serializer = Serializer()

    def get(self, object_id: str) -> Any:
        with suppress(FileNotFoundError):
            with open(f"{self._storage_path}/{object_id}", "r") as file:
                deserialized_data = self._serializer.deserialize(file.read())
                return pickle.loads(deserialized_data)

    def set(self, object_id: str, data: Any) -> None:
        pickled_data = pickle.dumps(data)
        # Serializing pickled data since file.write() accepts only string content but not bytes.
        serialized_data = self._serializer.serialize(pickled_data)
        with open(f"{self._storage_path}/{object_id}", "w") as file:
            file.write(serialized_data)

    @staticmethod
    def _init_storage(storage_path: str) -> None:
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
