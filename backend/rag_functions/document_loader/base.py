from abc import ABC, abstractmethod

class DocumentLoader(ABC):
    @abstractmethod
    def load_docs(self, file_path, user_owner=None):
        pass
