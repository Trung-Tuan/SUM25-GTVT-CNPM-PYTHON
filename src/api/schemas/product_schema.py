# api/schemas/product_schema.py
from marshmallow import Schema, fields

class ProductResponseSchema(Schema):
    """Schema đơn giản để serialize Product response"""
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    price = fields.Float()
    quantity = fields.Int()
    category = fields.Str()
    is_available = fields.Bool()
    image = fields.Str()
    rating = fields.Float()
    reviews = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    min_age = fields.Int()
    max_age = fields.Int()
    toy_name = fields.Str()
    brand = fields.Str()
    total_quantity = fields.Int()
    price_1_day = fields.Float()
    price_1_week = fields.Float()
    price_2_weeks = fields.Float()
    is_for_sale = fields.Bool()
    is_for_rent = fields.Bool()
    status = fields.Str()

class ProductListResponseSchema(Schema):
    """Schema cho response list products"""
    success = fields.Bool()
    products = fields.List(fields.Nested(ProductResponseSchema))
    message = fields.Str()