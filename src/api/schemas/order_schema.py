from marshmallow import Schema, fields, post_dump
from typing import List

class OrderItemResponseSchema(Schema):
    id = fields.Integer()
    product_id = fields.Integer()
    quantity = fields.Integer()
    unit_price = fields.Float()
    item_type = fields.String()
    rental_days = fields.Integer(allow_none=True)
    return_status = fields.String(allow_none=True)
    days_overdue = fields.Integer(allow_none=True)
    late_fee = fields.Float(allow_none=True)
    damage_fee = fields.Float(allow_none=True)
    total_price = fields.Float()

class OrderResponseSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    items = fields.Nested(OrderItemResponseSchema, many=True)
    total_amount = fields.Float()
    deposit_amount = fields.Float()
    discount_amount = fields.Float()
    final_amount = fields.Float()
    order_type = fields.String()
    rental_start_date = fields.DateTime(allow_none=True)
    rental_end_date = fields.DateTime(allow_none=True)
    expected_return_date = fields.DateTime(allow_none=True)
    actual_return_date = fields.DateTime(allow_none=True)
    order_status = fields.String()
    payment_status = fields.String()
    shipping_address = fields.String(allow_none=True)
    supplier_id = fields.Integer(allow_none=True)
    created_at = fields.DateTime()

class OrderListResponseSchema(Schema):
    orders = fields.Nested(OrderResponseSchema, many=True)

class PaymentResponseSchema(Schema):
    id = fields.Integer()
    order_id = fields.Integer()
    payment_method = fields.String()
    payment_amount = fields.Float()
    payment_status = fields.String()
    transaction_id = fields.String(allow_none=True)
    platform_fee = fields.Float()
    supplier_earnings = fields.Float()
    payment_date = fields.DateTime()
    refund_amount = fields.Float()
    refund_date = fields.DateTime(allow_none=True)

class CreateOrderRequestSchema(Schema):
    shipping_address = fields.String(required=True)
    order_type = fields.String(missing='buy')

class ProcessPaymentRequestSchema(Schema):
    payment_method = fields.String(required=True)
    transaction_id = fields.String(allow_none=True)

class RefundRequestSchema(Schema):
    refund_amount = fields.Float(required=True)
