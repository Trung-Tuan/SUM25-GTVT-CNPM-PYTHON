from marshmallow import Schema, fields, validate, ValidationError

class LoginSchema(Schema):
    user_name = fields.Str(required=True, validate=validate.Length(min=4))
    password = fields.Str(required=True, validate=validate.Length(min=6))

class RegisterSchema(Schema):
    user_name = fields.Str(required=True, validate=validate.Length(min=4))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    email = fields.Email(required=False, allow_none=True)

class UserDataSchema(Schema):
    id = fields.Int()
    user_name = fields.Str()
    email = fields.Email()
    phone = fields.Str()
    address = fields.Str()
    is_verified = fields.Bool()
    user_type = fields.Str()
    reward_points = fields.Int()

def validate_login_data(data: dict) -> dict:
    schema = LoginSchema()
    try:
        return schema.load(data)
    except ValidationError as e:
        raise ValidationError(f"Dữ liệu không hợp lệ: {e.messages}")

def validate_register_data(data: dict) -> dict:
    schema = RegisterSchema()
    try:
        return schema.load(data)
    except ValidationError as e:
        raise ValidationError(f"Dữ liệu không hợp lệ: {e.messages}")

def serialize_user(user):
    return {
        'id': user.id,
        'user_name': user.user_name,
        'email': user.email,
        'phone': user.phone,
        'address': user.address,
        'is_verified': user.is_verified,
        'user_type': user.user_type,
        'reward_points': user.reward_points
    }


