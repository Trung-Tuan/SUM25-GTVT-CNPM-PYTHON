from marshmallow import Schema, fields, post_dump
from typing import List

class CartItemResponseSchema(Schema):
    id = fields.Integer()
    product_id = fields.Integer()
    quantity = fields.Integer()
    unit_price = fields.Float()
    item_type = fields.String()
    rental_days = fields.Integer(allow_none=True)
    total_price = fields.Float()

class CartResponseSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    items = fields.Nested(CartItemResponseSchema, many=True)
    total_amount = fields.Float()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @post_dump
    def calculate_total(self, data, **kwargs):
        # Tính tổng tiền từ các items
        if 'items' in data:
            total = sum(item.get('total_price', 0) for item in data['items'])
            data['total_amount'] = total
        return data

class AddToCartRequestSchema(Schema):
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(missing=1)
    item_type = fields.String(missing='buy')
    rental_days = fields.Integer(allow_none=True)

class UpdateCartItemRequestSchema(Schema):
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    item_type = fields.String(missing='buy')

class RemoveFromCartRequestSchema(Schema):
    product_id = fields.Integer(required=True)
    item_type = fields.String(missing='buy')
