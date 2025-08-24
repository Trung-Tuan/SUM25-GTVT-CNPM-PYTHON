from flask import Blueprint, request, jsonify
from infrastructure.databases.mssql import get_db_session
from infrastructure.repositories.user_repository import UserRepository
from services.user_service import UserService

user_bp = Blueprint("user", __name__, url_prefix="/api")

def get_service():
    db = get_db_session()
    return UserService(UserRepository(db))

def format_user_data(user):
    return {
        "user_id": user.user_id,
        "user_name": user.user_name,
        "full_name": user.full_name,
        "email": user.email,
        "phone_number": user.phone_number,
        "address": user.address,
        "role_name": user.role_name
    }

@user_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        service = get_service()
        
        user = service.register(
            user_name=data['user_name'],
            password=data['user_password'],
            email=data['email']
        )
        
        if not user:
            return jsonify({"success": False, "message": "Username already exists"}), 400
        
        return jsonify({"success": True, "message": "Register successful"}), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        service = get_service()
        
        user = service.login(data['user_name'], data['user_password'])
        if not user:
            return jsonify({"success": False, "message": "Invalid username or password"}), 401
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": format_user_data(user)
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route("/update", methods=["PUT"])
def update_user():
    try:
        data = request.json
        service = get_service()
        
        updated_user = service.update_user(
            data['user_id'], 
            data['user_name'], 
            data['full_name'],
            data['user_password'], 
            data['address'], 
            data['email'],
            data['phone_number'], 
            data['role_name']
        )
        
        if not updated_user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        return jsonify({"success": True, "message": "User updated successfully"}), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@user_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    try:
        email = request.json.get("email")
        service = get_service()
        
        if not service.get_user_by_email(email):
            return jsonify({"success": False, "message": "Email not found"}), 404
        #send OTP
        return jsonify({"success": True, "message": "OTP sent to email"}), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400