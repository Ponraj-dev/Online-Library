# resources/user.py
import base64
from datetime import datetime
import bcrypt
from flask import request, jsonify, make_response, request, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, get_jwt,jwt_required,get_jwt_identity, set_access_cookies, unset_jwt_cookies
from sqlalchemy import func
from website import db
from .models import Admin,User,Token,UsersTime
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename


auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)




class UserRegistration(Resource):
    def post(self):

        try:
            image = request.files.get('image')
            if not image:
                return {"message": "Please upload a profile image"}, 400

            # Get other form data from request.form
            username = request.form.get('username')
            email = request.form.get('email')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            # Validate input data
            checkUser = User.query.filter_by(email=email).first()
            checkPassword = User.query.filter_by(username=username).first()

            print("Received data:", username, email, password1, password2,image)
            if checkUser :
                return {"message": "Email already exists"}, 400
            if checkPassword:
                return {"message": "Username already exists"}, 400
            # Hash password
            hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Save user to database
            new_user = User(username=username, email=email, password=hashed_password , profile_image=image.read())
            db.session.add(new_user)
            print("added")
            try:
                db.session.commit()
                return {"message": "User registered successfully"}, 201
            except Exception as e:
                db.session.rollback()  # Rollback if commit fails
                print("Database commit failed:", str(e))
                return {"message": "Failed to register user"}, 500
        except:
            return {"message":"some error may occurred"}



# API Resource for User Login

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = User.query.filter_by(username=username).first()
        if not username or not password:
            return {"message": "Please provide both username and password"}, 400

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):

            userlogging = UsersTime(UserId=user.id,ActiveStatus=True)
            print(user.login_time)
            user.login_time = datetime.utcnow().date()
            print("logged",user.login_time)

            db.session.add(userlogging)
            db.session.commit()
            access_token = create_access_token(identity=user.id)
            response = make_response({"message": "Logged in successfully", "role": "user","token":access_token}, 200)
            return response
        else:
            return {"message": "Invalid username or password"}, 401




class UserLogout(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()  # Retrieves the user identity from the JWT
        userlog = UsersTime.query.filter_by(UserId=user_id).order_by(UsersTime.id.desc()).first()

        if userlog and userlog.logout_time is None:
            userlog.logout_time = datetime.utcnow()
            userlog.ActiveStatus = False
            print(userlog.ActiveStatus, userlog.logout_time)
            db.session.commit()
            return {"message": "worked"}

        else:
            return {"message": "Some error occurred"}



class DeleteUser(Resource):
    @jwt_required()
    def delete(self, id):
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=id).first()
        if not user or current_user_id!="admin":
            return {"message": "Access denied"}, 403
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User removed"}, 201
        else:
            return{"message":"user not found"}, 500


#######################################................login_problem................#######################################################################

class AdminLogin(Resource):
    def post(self):
        data = request.get_json()
        adminId = data.get("adminId")
        adminPwd = data.get("adminPwd")

        if not adminId or not adminPwd:
            return {"message": "Please provide both adminId and adminPwd"}, 400

        admin = Admin.query.filter_by(adminId=adminId).first()
        if admin and check_password_hash(admin.adminPwd, adminPwd):
            access_token = create_access_token(identity=admin.adminId)
            response = make_response({"message": "Logged in successfully", "role": "admin","token":access_token}, 200)
            return response
        else:
            return {"message": "Invalid admin credentials"}, 401

# class CheckSession(Resource):
#     @jwt_required()
#     def get(self):
#         try:
#             user_id = get_jwt_identity()
#             # Assuming there's a consistent admin user with a known ID
#             is_admin = (user_id == "admin")  # Replace ADMIN_USER_ID with the actual admin user ID

#             print(f"CheckSession: user_id={user_id}, is_admin={is_admin}")  # Log for debugging

#             return {"isAuthenticated": True, "isAdmin": is_admin}, 200
#         except Exception as e:
#             print(f"CheckSession Error: {str(e)}")  # Log for debugging
#             return {"isAuthenticated": False, "isAdmin": False, "error": str(e)}, 500



def create_default_admin():
    admin = Admin.query.filter(
        (Admin.adminId == 'admin') |
        (Admin.adminEmail == 'admin1@example.com')
    ).first()

    if not admin:
        default_admin = Admin(
            adminId='admin',
            adminPwd=generate_password_hash('admin123', method='pbkdf2:sha256'),
            adminEmail='admin1@example.com'
        )
        db.session.add(default_admin)
        db.session.commit()
        print("admin created")
    else:
        # Optional: Log or handle the situation where the admin already exists
        print("Admin with the specified ID or email already exists.")

api.add_resource(UserRegistration, '/api/signup')
api.add_resource(UserLogin, '/api/login')
api.add_resource(UserLogout, '/api/logout')
api.add_resource(AdminLogin,"/api/adminlogin")
# api.add_resource(CheckSession, '/api/checkSession')
api.add_resource(DeleteUser,"/api/delete_user/<int:id>")
