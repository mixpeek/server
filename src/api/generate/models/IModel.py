from abc import ABC, abstractmethod

class IModel(ABC):
    @abstractmethod
    def run(self):
        pass