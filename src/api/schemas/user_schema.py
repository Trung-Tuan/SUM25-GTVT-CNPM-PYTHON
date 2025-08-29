from marshmallow import Schema, fields, validate, ValidationError, validates_schema

class LoginSchema(Schema):
    user_name = fields.Str(required=True, validate=validate.Length(min=4))
    user_password = fields.Str(required=True, validate=validate.Length(min=6))
    
        
class RegisterSchema(Schema):
    user_name = fields.Str(required=True, validate=validate.Length(min=4))
    user_password = fields.Str(required=True, validate=validate.Length(min=6))
    confirm_password = fields.Str(required=True, validate=validate.Length(min=6))
    email = fields.Email(required=True)
    
    @validates_schema
    def validate_passwords_match(self, data, **kwargs): # hứng tham số ngầm
        if data.get('user_password') != data.get('confirm_password'):
            raise ValidationError({"confirm_password": ["Mật khẩu không trùng khớp."]})
class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True)

