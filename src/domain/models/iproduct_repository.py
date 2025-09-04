from abc import ABC, abstractmethod
from .product import Product
from typing import List, Optional

class IProductRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Product]:
        pass
