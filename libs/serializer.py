import pickle
import codecs

from typing import Any


class Serializer:
    def __init__(self):
        self.encoding = "base64"

    def serialize(self, cls_instance: Any) -> str:
        return codecs.encode(pickle.dumps(cls_instance), self.encoding).decode()

    def deserialize(self, serialized_cls: str) -> Any:
        return pickle.loads(codecs.decode(serialized_cls.encode(), self.encoding))
