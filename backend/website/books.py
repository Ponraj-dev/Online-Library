import base64
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import bcrypt
from flask import request, jsonify, make_response, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, get_jwt_identity
from sqlalchemy import desc
from . import db
from .models import Admin, User, Token, Ebooks,Request,Rating  # Assuming Book model is defined in models.py
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import cache


books_bp = Blueprint('books', __name__)
api = Api(books_bp)

class BookCreation(Resource):
    @jwt_required()
    def post(self):
        try:
            # Debug: Check if JWT is recognized
            user_id = get_jwt_identity()
            print(f"User ID from JWT: {user_id}")

            image = request.files.get('image')
            if not image:
                return {"message": "Please upload a profile image"}, 400
            book = request.files.get('book')
            if not book:
                return {"message": "Please upload a book"}, 400

            # Get other form data from request.form
            bookname = request.form.get('bookname')
            authors = request.form.get('authors')
            genre = request.form.get('genre')
            description = request.form.get('description')

            print("Received data:", bookname, authors, genre, description)

            new_book = Ebooks(
                bookname=bookname,
                Authors=authors,
                genre=genre,
                Book_profile_image=image.read(),
                book=book.read(),
                description=description  # Assuming you want to associate the book with a user
            )
            db.session.add(new_book)
            print("Added book to session")
            try:
                cache.clear()
                db.session.commit()
                cache.clear()
                return {"message": "Book registered successfully"}, 201
            except Exception as e:
                db.session.rollback()  # Rollback if commit fails
                print("Database commit failed:", str(e))
                return {"message": "Failed to register book"}, 500
        except Exception as e:
            print("Unexpected error:", str(e))
            return {"message": "Some error occurred"}, 500



class BookPage(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True)
    def get(self, id=None):
        ebook = Ebooks.query.filter_by(id=id).first()
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()

        book_count = 0
        if user != None:
            print(user)
            book_count=user.book_count
        if not ebook:
            return {"message": "Book not found"}, 404

        ebooks_data = []
        rating_data =[]
        profile_image_base64 = base64.b64encode(ebook.Book_profile_image).decode('utf-8') if ebook.Book_profile_image else None
        book_base64 = None

        # Check if the book is requested or issued
        request_entry = Request.query.filter_by(ebook_id=ebook.id, user_id=current_user_id).order_by(desc(Request.id)).first()
        print(request_entry)
        status = "Available"
        pending = False
        issued = False

        if request_entry:
            pending = request_entry.is_requested and not request_entry.is_approved
            issued = request_entry.is_approved and not request_entry.is_retrieved
            if pending:
                status = "Pending"
            elif issued:
                status = "Issued"
                book_base64 = base64.b64encode(ebook.book).decode('utf-8') if ebook.book else None
        if current_user_id == 'admin':
            book_base64 = base64.b64encode(ebook.book).decode('utf-8') if ebook.book else None
        ebooks_data.append({
            "id": ebook.id,
            "bookname": ebook.bookname,
            "profile_image": profile_image_base64,
            "genre": ebook.genre.split(','),
            "Authors": ebook.Authors,
            "date_issued": ebook.date_issued,
            "return_by": ebook.return_by,
            "description": ebook.description,
            "book": book_base64,
            "status": status,
            "pending": pending,
            "issued": issued,
            "book_count":book_count
        })

        ratings = Rating.query.filter_by(ebook_id=id).all()
        if not ratings:
            average_rating = 0
        else:
            total_rating = sum([rating.value for rating in ratings])
            average_rating = total_rating / len(ratings)

        for rating in ratings:
            user = User.query.filter_by(id=rating.user_id).first()
            if user:
                rating_data.append({
                    "rating_value": rating.value,
                    "rating_description": rating.description,
                    "rated_by": user.username
                })

        return jsonify({"ebooks": ebooks_data, "bookpdf": book_base64,"rating": rating_data, "average_rating": average_rating})

class DeleteBook(Resource):
    @jwt_required()
    def delete(self, id):
        current_user_email = get_jwt_identity()
        if current_user_email != "admin":
            return jsonify({"message": "Unauthorized access"}), 403
        try:
            cache.clear()
            book = Ebooks.query.filter_by(id=id).first()
            if not book:
                return {"message": "Book not found"}, 404

            # Find and delete all requests related to this book
            # requests_to_delete = Request.query.filter_by(ebook_id=id).first()
            # for request in requests_to_delete:
            #     db.session.delete(request)

            db.session.delete(book)
            db.session.commit()
            cache.clear()
            return {"message": "Book and associated requests removed"}, 200

        except Exception as e:
            db.session.rollback()  # Rollback if commit fails
            print("Database commit failed:", str(e))
            return {"message": "Failed to remove book and associated requests"}, 500




class RequestBook(Resource):
    @jwt_required()
    def post(self, id):
        user_id = get_jwt_identity()
        # existing_request = Request.query.filter_by(user_id=user_id, ebook_id=id).first()
        # if existing_request.is_retrieved != True:
        #     return {"message": "Request already exists"}, 400
        user = User.query.filter_by(id=user_id).first()

        if user.book_count > 5 :
            return {"message": "you already have 5 books"}, 201
        try:
            new_request = Request(
            is_requested=True,
            user_id=user_id,
            ebook_id=id
        )
            cache.clear()
            db.session.add(new_request)
            db.session.commit()
            cache.clear()
            return {"message": "Book requested successfully"}, 201
        except Exception as e:
            db.session.rollback()  # Rollback if commit fails
            print("Database commit failed:", str(e))
            return {"message": "Failed to request book"}, 500


class ReturnBook(Resource):
    @jwt_required()
    def post(self):
        try:
            book_id = request.json.get('bookId')
            if not book_id:
                return {"message": "Book ID is required"}, 400

            request_instance = Request.query.filter_by(ebook_id=book_id, is_approved=True, is_retrieved=False).first()
            userId = request_instance.user_id
            user = User.query.filter_by(id=userId).first()

            if request_instance:
                request_instance.is_retrieved = True
                user.book_count -= 1
                cache.clear()
                db.session.commit()
                cache.clear()
                return {"message": "Book returned successfully"}, 200
            else:
                return {"message": "Request for the book not found or already returned"}, 404

        except Exception as e:
            db.session.rollback()
            print("Database commit failed:", str(e))
            return {"message": "Failed to return book"}, 500


class MyBooks(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True)
    def get(self):
        user_id = get_jwt_identity()
        my_books = []
        user_data = Request.query.filter_by(user_id=user_id, is_approved=True,is_retrieved=False).all()

        print(user_data) # Fetch only approved books
        for book in user_data:
            current_date = datetime.utcnow()
            days_left = (book.due_date - current_date).days if book.due_date else None

                # Format due date as 'Fri, 09 Aug 09:15'
            due_date_formatted = book.due_date.strftime('%a, %d %b %H:%M') if book.due_date else None
            print(book.ebook_id)
            if book.ebook_id :
                ebook = Ebooks.query.filter_by(id=book.ebook_id).first() # Use the relationship to get the ebook
                profile_image_base64 = base64.b64encode(ebook.Book_profile_image).decode('utf-8') if ebook.Book_profile_image else None

                my_books.append({
                    "id": ebook.id,
                    "bookname": ebook.bookname,
                    "profile_image": profile_image_base64,
                    "genre": ebook.genre.split(','),
                    "Authors": ebook.Authors,
                    "date_issued": ebook.date_issued,
                    "due_date": due_date_formatted,
                    "days_left": days_left,
                    "description": ebook.description,
                })
        return jsonify({"my_books": my_books})


class EditBook(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True)
    def get(self, book_id=None):
        current_user_email = get_jwt_identity()
        if current_user_email != "admin":
            return jsonify({"message": "Unauthorized access"}), 403
        try:
            if not book_id:
                return {"message": "Invalid book ID"}, 400
            ebook = Ebooks.query.filter_by(id=book_id).first()

            if ebook:
                profile_image_base64 = base64.b64encode(ebook.Book_profile_image).decode('utf-8') if ebook.Book_profile_image else None
                book_data = {
                    "id": ebook.id,
                    "bookname": ebook.bookname,
                    "authors": ebook.Authors,
                    "genre": ebook.genre,
                    "description": ebook.description,
                    "Book_profile_image": profile_image_base64,
                }
                return jsonify({"ebook": book_data})
            else:
                return {"message": "Book not found"}, 404
        except Exception as e:
            print("Error fetching book profile:", str(e))
            return {"message": "Failed to fetch book profile"}, 500

    @jwt_required()
    def post(self, book_id=None):
        try:
            if not book_id:
                return {"message": "Invalid book ID"}, 400

            ebook = Ebooks.query.get(book_id)
            if not ebook:
                return {"message": "Book not found"}, 404

            image = request.files.get('image')
            book = request.files.get('book')
            bookname = request.form.get('bookname')
            authors = request.form.get('authors')
            genre = request.form.get('genre')
            description = request.form.get('description')

            print("Received data:", bookname, authors, genre, description)

            if bookname:
                ebook.bookname = bookname
            if authors:
                ebook.Authors = authors
            if genre:
                ebook.genre = genre
            if description:
                ebook.description = description
            if book:
                ebook.book = book.read()
            if image:
                ebook.Book_profile_image = image.read()

            try:
                cache.clear()
                db.session.commit()
                cache.clear()
                return {"message": "Edit Book successfully"}, 201
            except Exception as e:
                db.session.rollback()
                print("Database commit failed:", str(e))
                return {"message": "Failed to edit book"}, 500
        except Exception as e:
            print("Error in post method:", str(e))
            return {"message": "An error occurred"}, 500

class BookRating(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        value = data.get('value')
        description = data.get('description')
        ebook_id = data.get('ebook_id')

        print(value, description)

        if not value or not description or not ebook_id:
            return jsonify({"error": "Missing data"}), 400

        if value < 1 or value > 5:
            return jsonify({"error": "Rating value must be between 1 and 5"}), 400

        user = User.query.get(user_id)
        print(user)
        if not user:
            return jsonify({"error": "User not found"}), 404
        ebook = Ebooks.query.get(ebook_id)
        print(ebook)
        if not ebook:
            return jsonify({"error": "eBook not found"}), 404

        new_rating = Rating(value=value, description=description, user_id=user_id, ebook_id=ebook_id)
        db.session.add(new_rating)
        try:
            cache.clear()
            db.session.commit()
            cache.clear()
            return {"message": "Rating submitted successfully!"}, 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

api.add_resource(DeleteBook, "/api/deletebook/<int:id>")
api.add_resource(BookCreation, "/api/bookcreation")
api.add_resource(BookPage,"/api/bookspage/<int:id>" ,"/api/purchasePage/<int:id>")
api.add_resource(RequestBook,"/api/requestbook/<int:id>")
api.add_resource(ReturnBook,"/api/returnbook/")
api.add_resource(MyBooks, "/api/mybooks")
api.add_resource(EditBook, '/api/EditBook/<int:book_id>')
api.add_resource(BookRating, "/api/ratebook")