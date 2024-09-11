import base64
import bcrypt
from flask import request, jsonify, make_response, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, get_jwt_identity
from sqlalchemy import and_, desc
from . import db
from .models import Admin, Ebooks, Rating, User, Token,Request,Section  # Assuming Book model is defined in models.py
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import cache

section_bp = Blueprint('section', __name__)
api = Api(section_bp)

class sectionCreation(Resource):
    @jwt_required()
    def post(self):
        try:
            # Debug: Check if JWT is recognized
            user_id = get_jwt_identity()
            print(f"User ID from JWT: {user_id}")

            image = request.files.get('image')
            if not image:
                return {"message": "Please upload a profile image"}, 400

            # Get other form data from request.form
            name = request.form.get('name')
            genre = request.form.get('genre')
            description = request.form.get('description')

            print("Received data:",name, genre)

            new_book = Section(
                name=name,
                genre=genre,
                image=image.read(), # Assuming you want to associate the book with a user
                description=description
            )
            db.session.add(new_book)
            print("Added section to session")

            try:
                cache.clear()
                db.session.commit()
                cache.clear()
                return {"message": "section registered successfully"}, 201
            except Exception as e:
                db.session.rollback()  # Rollback if commit fails
                print("Database commit failed:", str(e))
                return {"message": "Failed to register section"}, 500
        except Exception as e:
            print("Unexpected error:", str(e))
            return {"message": "Some error occurred"}, 500

class SectionView(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True)
    def get(self):
        sections = Section.query.all()
        sections_data = []
        for section in sections:
            profile_image_base64 = base64.b64encode(section.image).decode('utf-8') if section.image else None
            sections_data.append({
                "id": section.id,
                "name": section.name,
                "section_profile_image": profile_image_base64,
                "genre": section.genre,
            })
        return jsonify({"sections": sections_data})

class SectionPage(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True)
    def get(self, id):
        section = Section.query.filter_by(id=id).first()
        if not section:
            return jsonify({"sections": []})

        books_data = []
        for book in section.books:
            request_entry = Request.query.filter_by(ebook_id=book.id).order_by(desc(Request.id)).first()
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
            profile_image_base64 = base64.b64encode(book.Book_profile_image).decode('utf-8') if book.Book_profile_image else None
            books_data.append({
                "id": book.id,
                "title": book.bookname,
                "author": book.Authors,
                "Book_image": profile_image_base64,
                "status": status,
                "pending": pending,
                "issued": issued
            })


        profile_image_base64 = base64.b64encode(section.image).decode('utf-8') if section.image else None

        section_data = {
            "id": section.id,
            "name": section.name,
            "section_profile_image": profile_image_base64,
            "genre": section.genre,
            "description": section.description,
        }
        return jsonify({"sections": [section_data],"ebooks":books_data})

class DeleteSection(Resource):
    @jwt_required()
    def delete(self, id):
        try:
            # Find the book to delete
            section = Section.query.filter_by(id=id).first()
            if not section:
                return {"message": "Book not found"}, 404

            # Find and delete all requests related to this book
            # requests_to_delete = Request.query.filter_by(ebook_id=id).first()
            # for request in requests_to_delete:
            #     db.session.delete(request)

            # Delete the book
            db.session.delete(section)
            db.session.commit()
            return {"message": "Book and associated requests removed"}, 200

        except Exception as e:
            db.session.rollback()  # Rollback if commit fails
            print("Database commit failed:", str(e))
            return {"message": "Failed to remove book and associated requests"}, 500


class AddBooks(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True)
    def get(self,section_id=None):
        if section_id:
            section = Section.query.filter_by(id=section_id).first()
        else:
            section = Section.query.all()
        if not section:
            return jsonify({"sections": []})

        ebooks = Ebooks.query.all()
        ebooks_data = []
        for ebook in ebooks:
            ratings = Rating.query.filter_by(ebook_id=ebook.id).all()

            if not ratings:
                total_rating = 0
            else:
                total_rating = sum([rating.value for rating in ratings])
                print("total value",total_rating)

            if total_rating == 0:
                average_rating = 0
            else:
                average_rating = total_rating / len(ratings)
            profile_image_base64 = base64.b64encode(ebook.Book_profile_image).decode('utf-8') if ebook.Book_profile_image else None
            book_base64 = base64.b64encode(ebook.book).decode('utf-8') if ebook.book else None
            is_in_section = any(book.id == ebook.id for book in section.books) if section_id else None
            ebooks_data.append({
                "id": ebook.id,
                "bookname": ebook.bookname,
                "profile_image": profile_image_base64,
                "genre": ebook.genre.split(','),
                "Authors": ebook.Authors,
                "date_issued": ebook.date_issued,
                "return_by": ebook.return_by,
                "description": ebook.description,
                "book":book_base64,
                "in_section": is_in_section,
                "average_rating":average_rating
            })
        return jsonify({"ebooks_data": ebooks_data})

    @jwt_required()
    def post(self):
        data = request.get_json()
        section_id = data.get('sectionId')
        book_id = data.get('bookid')

        if not section_id or not book_id:
            return {'message': 'Section ID and Book ID are required.'}, 400

        section = Section.query.get(section_id)
        book = Ebooks.query.get(book_id)

        if not section or not book:
            return {'message': 'Invalid Section ID or Book ID.'}, 404

        section.books.append(book)
        cache.clear()
        db.session.commit()
        cache.clear()

        return {'message': 'Book added to section successfully.'}, 201



class RemoveBook(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        section_id = data.get('sectionId')
        book_id = data.get('bookid')

        if not section_id or not book_id:
            return {'message': 'Section ID and Book ID are required.'}, 400

        section = Section.query.get(section_id)
        book = Ebooks.query.get(book_id)

        if not section or not book:
            return {'message': 'Invalid Section ID or Book ID.'}, 404

        if book not in section.books:
            return {'message': 'Book is not in the section.'}, 404
        if book not in section.books:
            return {'message': 'Book is not in the section.'}, 404
        cache.clear()

        section.books.remove(book)
        db.session.commit()
        cache.clear()

        return {'message': 'Book removed from section successfully.'}, 200

class EditSection(Resource):
    @jwt_required()
    def get(self, section_id=None):
        current_user_email = get_jwt_identity()
        if current_user_email != "admin":
            return jsonify({"message": "Unauthorized access"}), 403
        try:
            if not section_id:
                return {"message": "Invalid book ID"}, 400
            section = Section.query.filter_by(id=section_id).first()
            print(section)

            if section:
                profile_image_base64 = base64.b64encode(section.image).decode('utf-8') if section.image else None
                book_data = {
                    "id": section.id,
                    "name": section.name,
                    "genre": section.genre,
                    "image": profile_image_base64,
                    "description":section.description
                }
                return jsonify({"section": book_data})
            else:
                return {"message": "Book not found"}, 404
        except Exception as e:
            print("Error fetching book profile:", str(e))
            return {"message": "Failed to fetch book profile"}, 500

    @jwt_required()
    def post(self, section_id=None):
        try:
            if not section_id:
                return {"message": "Invalid book ID"}, 400

            section = Section.query.get(section_id)
            if not section:
                return {"message": "Book not found"}, 404

            image = request.files.get('image')
            name = request.form.get('name')
            genre = request.form.get('genre')
            description = request.form.get('description')
            if name:
                section.name =name
            if genre:
                section.genre = genre
            if description:
                section.description = description
            if image:
                section.image = image.read()

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

class Search(Resource):
    @jwt_required()
    @cache.cached(timeout=60, query_string=True)
    def get(self):
        category = request.args.get('category', '')
        query = request.args.get('query', '')
        section_id = request.args.get('sectionId', '')

        filters = []
        if category:
            filters.append(Ebooks.genre.ilike(f'%{category}%'))
        if query:
            filters.append(Ebooks.bookname.ilike(f'%{query}%'))
        # if section_id:
        #     filters.append(Ebooks.Section.any(id=section_id))

        ebooks = Ebooks.query.filter(and_(*filters)).all()
        ebooks_list = []

        section_books = []
        # if section_id:
        #     section = Section.query.filter_by(id=section_id).first()
        #     section_books = section.books if section else []

        for ebook in ebooks:
            ratings = Rating.query.filter_by(ebook_id=ebook.id).all()
            if not ratings:
                total_rating = 0
            else:
                total_rating = sum([rating.value for rating in ratings])
                print("total value",total_rating)

            if total_rating == 0:
                average_rating = 0
            else:
                average_rating = total_rating / len(ratings)
            profile_image_base64 = base64.b64encode(ebook.Book_profile_image).decode('utf-8') if ebook.Book_profile_image else None
            book_base64 = base64.b64encode(ebook.book).decode('utf-8') if ebook.book else None
            is_in_section = any(book.id == ebook.id for book in section_books)
            ebooks_list.append({
                "id": ebook.id,
                "bookname": ebook.bookname,
                "profile_image": profile_image_base64,
                "genre": ebook.genre.split(','),
                "Authors": ebook.Authors,
                "date_issued": ebook.date_issued,
                "return_by": ebook.return_by,
                "description": ebook.description,
                "book": book_base64,
                "in_section": is_in_section,
                "average_rating":average_rating
            })

        return jsonify({'ebooks_data': ebooks_list})



api.add_resource(Search, '/api/searchBooks')
api.add_resource(sectionCreation,"/api/sectionCreation")
api.add_resource(SectionView,"/api/sectionsDashboard" ,"/api/AllSection")
api.add_resource(SectionPage, "/api/sectionspage/<int:id>")
api.add_resource(DeleteSection, "/api/deletesection/<int:id>")
api.add_resource(AddBooks,'/api/AddBooksToSection/<int:section_id>','/api/addbook',"/api/search/")
api.add_resource(RemoveBook,"/api/removebook")
api.add_resource(EditSection, '/api/Editsection/<int:section_id>')