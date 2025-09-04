from domain.models.product import Product
from domain.models.iproduct_repository import IProductRepository
from typing import List

class ProductService:
    def __init__(self, repository: IProductRepository):
        self.repository = repository
    
    def get_all_products(self) -> List[Product]:
        return self.repository.get_all()
