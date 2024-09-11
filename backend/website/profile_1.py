import base64
import bcrypt
from flask import request, jsonify, make_response, request, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, get_jwt,jwt_required,get_jwt_identity, set_access_cookies, unset_jwt_cookies
from . import db
from .models import Admin,User,Token
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from . import cache

profile_bp = Blueprint('profile', __name__)
api = Api(profile_bp)




class UserProfile(Resource):
    @jwt_required()
    def get(self, user_id=None):
        try:
            if user_id is None:
                user_id = get_jwt_identity()
            user = User.query.filter_by(id=user_id).first()
            print(user_id)

            if user:
                profile_image_base64 = base64.b64encode(user.profile_image).decode('utf-8') if user.profile_image else None
                user_data = {
                    "id":user.id,
                    "username": user.username,
                    "email": user.email,
                    "book_count":user.book_count,
                    "profile_image": profile_image_base64,  # Assuming you handle image conversion elsewhere
                }

                return jsonify({"user": user_data})
            else:
                return {"message": "User not found"}, 404
        except Exception as e:
            print("Error fetching user profile:", str(e))
            return {"message": "Failed to fetch user profile"}, 500


class EditProfile(Resource):
    def get(self,user_id=None):
        try:
            if user_id is None:
                user_id = get_jwt_identity()
            user = User.query.filter_by(id=user_id).first()
            if user:
                profile_image_base64 = base64.b64encode(user.profile_image).decode('utf-8') if user.profile_image else None
                user_data = {
                    "id":user.id,
                    "username": user.username,
                    "email": user.email,
                    "profile_image": profile_image_base64,  # Assuming you handle image conversion elsewhere
                }
                return jsonify({"user": user_data})
            else:
                return {"message": "User not found"}, 404
        except Exception as e:
            print("Error fetching user profile:", str(e))
            return {"message": "Failed to fetch user profile"}, 500



    def post(self,user_id=None):
        try:
            image = request.files.get('image')
            if not image:
                return {"message": "Please upload a profile image"}, 400

            user = User.query.get(user_id)

            # Get other form data from request.form
            username = request.form.get('username')
            email = request.form.get('email')
            password1 = request.form.get('password1')
            user.profile_image = image.read()

            # Validate input data
            # Hash password
            if username:
                user.username = username
            if email:
                user.email = email
            if password1:
                hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user.password = hashed_password
            # Save user to database
            try:
                cache.clear()
                db.session.commit()
                cache.clear()
                return {"message": "User registered successfully"}, 201
            except Exception as e:
                db.session.rollback()  # Rollback if commit fails
                print("Database commit failed:", str(e))
                return {"message": "Failed to register user"}, 500
        except:
            return {"message":"some error may occurred"}





api.add_resource(UserProfile,"/api/profile/", "/api/profile/<int:user_id>")

api.add_resource(EditProfile,"/api/Editprofile/<int:user_id>")