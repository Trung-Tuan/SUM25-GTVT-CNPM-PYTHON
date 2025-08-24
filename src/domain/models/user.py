
class User:
    
    def __init__(self, user_name: str, password: str, email: str = None, phone: str = None, address: str = None, is_verified: bool = False, user_type: str = "renter",reward_points: int = 0, id: int = None):
        self.id = id
        self.user_name = user_name
        self.password = password
        self.email = email
        self.phone = phone
        self.address = address
        self.is_verified = is_verified
        self.user_type = user_type
        self.reward_points = reward_points
        self.created_at = None
        self.updated_at = None
