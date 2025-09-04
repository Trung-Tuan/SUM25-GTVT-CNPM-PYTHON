class Product:
    
    def __init__(
        self,
        name: str,
        description: str = None,
        price: float = 0.0,
        quantity: int = 0,
        category: str = None,
        is_available: bool = True,
        id: int = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.category = category
        self.is_available = is_available
        self.created_at = None
        self.updated_at = None