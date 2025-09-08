from abc import ABC, abstractmethod
from .product import Product
from typing import List, Optional

class IProductRepository(ABC):
    @abstractmethod
    def get_all_products_with_filter(self, category_id=None, min_price=None, max_price=None, age_range=None, sort_by=None, sort_order="asc") -> List[Product]:
        pass
    
    def get_featured(self) -> List[Product]:
        pass

    def get_categories(self) -> List[str]:
        pass
    
