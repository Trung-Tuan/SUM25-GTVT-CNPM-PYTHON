from domain.models.iproduct_repository import IProductRepository
from domain.models.product import Product  # domain entity
from infrastructure.models.toys_model import Toys  # ORM
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import desc

class ProductRepository(IProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all_products_with_filter(
        self,
        category_id: int = None,
        min_price: float = None,
        max_price: float = None,
        age_range: str = None,
        sort_by: str = None,
        sort_order: str = "asc" 
    ) -> List[Product]:
        query = self.session.query(Toys)  # bắt đầu query động

        # === FILTERS ===
        if category_id is not None:
            query = query.filter(Toys.category == category_id) #add thêm điều kiện

        if min_price is not None:
            query = query.filter(Toys.price_sale >= min_price)

        if max_price is not None:
            query = query.filter(Toys.price_sale <= max_price)

        if age_range:
            try:
                if "-" in age_range:
                    min_age, max_age = map(int, age_range.split("-"))
                    query = query.filter(
                        Toys.min_age <= max_age,
                        Toys.max_age >= min_age
                    )
                else:
                    query = query.filter(
                        Toys.max_age >= 13
                    )
            except ValueError:
                pass

        # === SORTING ===
        if sort_by == "price":
            col = Toys.price_sale
        elif sort_by == "name":
            col = Toys.name
        elif sort_by == "created_at":
            col = Toys.created_at
        else:
            col = None

        if col is not None:
            if sort_order.lower() == "desc":
                query = query.order_by(col.desc())
            else:
                query = query.order_by(col.asc())

        product_models = query.all()

        return [
            Product(
                id=m.id,
                name=m.name,
                description=m.description,
                category=m.category,
                price=m.price_sale,
                quantity=m.available_quantity,
                is_available=(m.is_active == 1),
                image=m.image,
                rating=m.rating,
                reviews=m.reviews,
                created_at=m.created_at,
                updated_at=m.updated_at,
                min_age=m.min_age,
                max_age=m.max_age,
                toy_name=m.toy_name,
                brand=m.brand,
                total_quantity=m.total_quantity,
                price_1_day=m.price_1_day,
                price_1_week=m.price_1_week,
                price_2_weeks=m.price_2_weeks,
                is_for_sale=m.is_for_sale,
                is_for_rent=m.is_for_rent,
                status=m.status,
            )
            for m in product_models
        ]


    
    def get_featured(self) -> List[Product]:
        featured_models = (
            self.session.query(Toys)
            .order_by(desc(Toys.total_quantity - Toys.available_quantity))
            .limit(9)
            .all()
        )
        return [
            Product(
                id=product_model.id,
                name=product_model.name,
                description=product_model.description,
                category=product_model.category,
                price=product_model.price_sale,
                quantity=product_model.available_quantity,
                is_available=(product_model.is_active == 1),
                image=product_model.image,
                rating=product_model.rating,
                reviews=product_model.reviews,
                created_at=product_model.created_at,
                updated_at=product_model.updated_at,
                min_age=product_model.min_age,
                max_age=product_model.max_age,
                toy_name=product_model.toy_name,
                brand=product_model.brand,
                total_quantity=product_model.total_quantity,
                price_1_day=product_model.price_1_day,
                price_1_week=product_model.price_1_week,
                price_2_weeks=product_model.price_2_weeks,
                is_for_sale=product_model.is_for_sale,
                is_for_rent=product_model.is_for_rent,
                status=product_model.status,
            )
            for product_model in featured_models
        ]
    
    def get_categories(self) -> List[str]:
        categories = self.session.query(Toys.category).distinct().all() # distinct đảm bảo không trùng lặp
        return [category[0] for category in categories]
