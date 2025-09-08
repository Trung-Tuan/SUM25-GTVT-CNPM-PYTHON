from domain.models.product import Product
from domain.models.iproduct_repository import IProductRepository
from typing import List

class ProductService:
    def __init__(self, repository: IProductRepository):
        self.repository = repository
    
    def get_all_products_with_filter(self, category_id=None, min_price=None, max_price=None, age_range=None, sort_by=None, sort_order="asc") -> List[Product]:
        return self.repository.get_all_products_with_filter(
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            age_range=age_range,
            sort_by=sort_by,
            sort_order=sort_order
        )
    
    def get_featured_products(self) -> List[Product]:
        return self.repository.get_featured()

    def get_all_categories(self) -> List[str]:
        return self.repository.get_categories()