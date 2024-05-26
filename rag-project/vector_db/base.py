from abc import ABC, abstractmethod

class VectorDB(ABC):
    @abstractmethod
    def store_embeddings(self, docs, user_owner=None):
        pass
