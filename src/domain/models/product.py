class Product:
    def __init__(
        self,
        name: str,
        description: str = None,
        price: float = 0.0,
        quantity: int = 0,
        category: str = None,
        is_available: bool = True,
        id: int = None,
        image: str = None,
        rating: float = 0.0,
        reviews: int = 0,
        created_at=None,
        updated_at=None,
        min_age: int = None,
        max_age: int = None,
        toy_name: str = None,
        brand: str = None,
        total_quantity: int = 0,
        price_1_day: float = 0.0,
        price_1_week: float = 0.0,
        price_2_weeks: float = 0.0,
        is_for_sale: bool = False,
        is_for_rent: bool = False,
        status: str = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.category = category
        self.is_available = is_available
        self.image = image
        self.rating = rating
        self.reviews = reviews
        self.created_at = created_at
        self.updated_at = updated_at
        self.min_age = min_age
        self.max_age = max_age
        self.toy_name = toy_name
        self.brand = brand
        self.total_quantity = total_quantity
        self.price_1_day = price_1_day
        self.price_1_week = price_1_week
        self.price_2_weeks = price_2_weeks
        self.is_for_sale = is_for_sale
        self.is_for_rent = is_for_rent
        self.status = status