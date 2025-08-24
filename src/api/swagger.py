from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from api.schemas.user_schema import RegisterSchema, LoginSchema, ChangePassword, UserDataSchema 

spec = APISpec(
    title="Login API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Đăng ký schema để tự động sinh model
spec.components.schema("Register", schema=RegisterSchema)
spec.components.schema("Login", schema=LoginSchema)
spec.components.schema("ChangePassword", schema=ChangePassword)
spec.components.schema("UserData", schema=UserDataSchema)