from typing import Any
from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    @abstractmethod
    def set(self, object_id: str, data: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, object_id: str) -> Any:
        raise NotImplementedError
