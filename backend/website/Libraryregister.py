import base64
from datetime import datetime, timedelta
import bcrypt
from flask import request, jsonify, make_response, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, get_jwt_identity
from . import cache
from . import db
from .models import Admin, User, Token, Ebooks,Request
from werkzeug.security import generate_password_hash, check_password_hash

register_bp = Blueprint('register', __name__)
api = Api(register_bp)

class LibraryRegister(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True)
    def get(self):
        requests = Request.query.all()

        request_data = []
        issuedBook_data = []

        for req in requests:
            user = User.query.filter_by(id=req.user_id).first()
            ebook = Ebooks.query.filter_by(id=req.ebook_id).first()
            if user and ebook:
                if req.is_requested and not req.is_approved:
                    request_data.append({
                        "id": req.id,
                        "requested_book": ebook.bookname,
                        "requested_user_name": user.username,
                        "requested_date": req.request_date.strftime("%Y-%m-%d %H:%M:%S"),
                    })
                elif req.is_approved and not req.is_retrieved:
                    issuedBook_data.append({
                        "id": req.id,
                        "issuedBook_name": ebook.bookname,
                        "issued_user_name": user.username,
                        "approved_date": req.approved_date.strftime("%Y-%m-%d %H:%M:%S"),
                        "due_date": req.due_date.strftime("%Y-%m-%d %H:%M:%S"),
                    })

        return jsonify({"requests": request_data, "issued": issuedBook_data})


class ApproveBook(Resource):
    @jwt_required()
    def post(self, requestId=None):
        try:
            if not requestId:
                return jsonify({"message": "Request ID is required"}), 400

            req_instance = Request.query.filter_by(id=requestId).first()
            userId = req_instance.user_id
            user = User.query.filter_by(id=userId).first()

            if user.book_count is None:
                user.book_count = 0

            if not req_instance:
                return jsonify({"message": "Request not found"}), 404

            if req_instance.is_requested and not req_instance.is_approved:
                req_instance.is_approved = True
                user.book_count += 1
                req_instance.approved_date = datetime.utcnow()
                req_instance.due_date = req_instance.approved_date + timedelta(days=7)

            elif req_instance.is_approved and not req_instance.is_retrieved:
                req_instance.is_retrieved = True
                user.book_count -= 1
                req_instance.retrieved_date = datetime.utcnow()



            print("no error till")
            cache.clear()
            db.session.commit()
            cache.clear()
            return {"message":"Book approved successfully"}, 201

        except Exception as e:
            db.session.rollback()
            print("Database commit failed:", str(e))
            return {"message": "Failed to approve request"}, 201



class RequestReject(Resource):
    @jwt_required()
    def delete(self):
        try:
            request_id = request.json.get('requestId')

            if not request_id:
                return jsonify({"message": "Request ID is required"}), 400

            req_instance = Request.query.filter_by(id=request_id).first()
            if not req_instance:
                return jsonify({"message": "Request not found"}), 404
            cache.clear()


            db.session.delete(req_instance)
            db.session.commit()
            cache.clear()

            return {"message": "User rejected successfully"}, 201

        except Exception as e:
            db.session.rollback()
            print("Database commit failed:", str(e))
            return {"message": "Failed to reject request"}, 500

class RetrieveBook(Resource):
    @jwt_required()
    def post(self, requestId=None):
        try:
            if not requestId:
                return jsonify({"message": "Request ID is required"}), 400

            req_instance = Request.query.get(requestId)
            userId = req_instance.user_id
            user = User.query.filter_by(id=userId).first()

            if user.book_count is None:
                user.book_count = 0

            if not req_instance:
                return jsonify({"message": "Request not found"}), 404

            if req_instance.is_requested and not req_instance.is_approved:
                req_instance.is_approved = True
                user.book_count  += 1
                req_instance.approved_date = datetime.utcnow()
                req_instance.due_date = req_instance.approved_date + timedelta(days=7)
            elif req_instance.is_approved and not req_instance.is_retrieved:
                req_instance.is_retrieved = True
                user.book_count -= 1
                req_instance.retrieved_date = datetime.utcnow()
            cache.clear()


            db.session.commit()
            cache.clear()
            return {"message": "Book Retrieved successfully"}, 201

        except Exception as e:
            db.session.rollback()
            print("Database commit failed:", str(e))
            return {"message": "failed to retrieved "}, 201

api.add_resource(ApproveBook, "/api/libraryregister/approvebook/<int:requestId>")
api.add_resource(RequestReject, "/api/requestreject")
api.add_resource(LibraryRegister, "/api/libraryregister")
api.add_resource(RetrieveBook,"/api/libraryregister/retrieve/<int:requestId>")