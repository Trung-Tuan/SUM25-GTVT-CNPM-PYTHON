from infrastructure.databases.mssql import init_mssql
from infrastructure.models import categories_model, users_model, messages_model, order_items_model, orders_model, payments_model, revenue_tracking_model, reviews_model, reward_transactions_model, shipping_tracking_model,toy_verifications_model, toys_model,vouchers_model
# nhớ xóa todo_model 
def init_db(app):
    init_mssql(app)
    
from infrastructure.databases.mssql import Base