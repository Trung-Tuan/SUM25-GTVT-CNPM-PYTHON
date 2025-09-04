from flask import Blueprint, request, jsonify
from infrastructure.databases.mssql import get_db_session
from api.schemas.user_schema import RegisterSchema, LoginSchema
from infrastructure.repositories.user_repository import UserRepository
from services.user_service import UserService

user_bp = Blueprint("user", __name__, url_prefix="/api") 

def get_service():
    db = get_db_session()
    return UserService(UserRepository(db))

def format_user_data(user):
    return {
        "user_id": user.id,              
        "user_name": user.user_name,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,             
        "address": user.address,
        "role_name": user.user_type
    }

@user_bp.route("/register", methods=["POST"])
def register():
    try:
        schema = RegisterSchema()
        data = schema.load(request.json)

        service = get_service()
        
        user = service.register(
            user_name=data['user_name'],
            password=data['user_password'],
            # confirm_password=data['confirm_password'],
            email=data['email']
        )
        
        if not user:
            return jsonify({"success": False, "message": "Tài khoản đã tồn tại"}), 400
        
        return jsonify({"success": True, "message": "Đăng ký thành công"}), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route("/login", methods=["POST"])
def login():
    try:
        schema = LoginSchema()
        data = schema.load(request.json)

        service = get_service()
        
        user = service.login(data['user_name'], data['user_password'])
        if not user:
            return jsonify({"success": False, "message": "Sai tài khoản hoặc mật khẩu"}), 401
        
        return jsonify({
            "success": True,
            "message": "Đăng nhập thành công",
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
