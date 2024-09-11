from datetime import timedelta
from website import db
from flask_login import UserMixin
from flask import Flask
from flask_cors import CORS
from sqlalchemy.sql import func
from . import db
# Define the association table for many-to-many relationship
# Define the association table for many-to-many relationship

# Define the association table for the many-to-many relationship
section_books = db.Table('section_books',
    db.Column('section_id', db.Integer, db.ForeignKey('section.id'), primary_key=True),
    db.Column('ebook_id', db.Integer, db.ForeignKey('ebooks.id'), primary_key=True)
)

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    adminId = db.Column(db.Text, nullable=False)
    adminEmail = db.Column(db.String(150), unique=True)
    adminPwd = db.Column(db.String(150), nullable=False)
    # Define the one-to-many relationship between Admin and Ebook

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.LargeBinary, nullable=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    book_count = db.Column(db.Integer, default=0)
    login_time =  db.Column(db.DateTime(timezone=True))

    # Define relationships
    ratings = db.relationship('Rating', back_populates='user')
    requests = db.relationship('Request', back_populates='user')

class Ebooks(db.Model, UserMixin):
    __tablename__ = 'ebooks'
    id = db.Column(db.Integer, primary_key=True)
    Book_profile_image = db.Column(db.Text, nullable=False)
    bookname = db.Column(db.Text, nullable=False)
    genre = db.Column(db.Text, nullable=False)
    book = db.Column(db.LargeBinary, nullable=False)
    Authors = db.Column(db.Text, nullable=False)
    date_issued = db.Column(db.DateTime(timezone=True), default=func.now())
    return_by = db.Column(db.DateTime)
    description = db.Column(db.String(500), unique=True)
    # Define relationships
    requests = db.relationship('Request', back_populates='ebook')
    ratings = db.relationship('Rating', back_populates='ebook')
    Section = db.relationship('Section', secondary=section_books, back_populates='books')


    def set_genres(self, genres_list):
        self.genre = ','.join(genres_list)

    def get_genres(self):
        return self.genre.split(',')

class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

class Section(db.Model, UserMixin):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    genre = db.Column(db.Text, unique=True)
    description = db.Column(db.String(500),nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    books = db.relationship('Ebooks', secondary=section_books, back_populates='Section')

class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)

    # Status columns
    is_requested = db.Column(db.Boolean, default=True, nullable=False)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    is_retrieved = db.Column(db.Boolean, default=False, nullable=False)
    # Timestamps
    request_date = db.Column(db.DateTime(timezone=True), default=func.now())
    approved_date = db.Column(db.DateTime(timezone=True))
    retrieved_date = db.Column(db.DateTime(timezone=True))
    due_date = db.Column(db.DateTime)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebooks.id'))

    # Relationships
    user = db.relationship('User', back_populates='requests')
    ebook = db.relationship('Ebooks', back_populates='requests')

#..........for charts.......

def get_request_counts_by_genre():
    results = db.session.query(
        Ebooks.genre, func.count(Request.id)
    ).join(Request).group_by(Ebooks.genre).all()
    return results

def user_growth():
    # Get the count of users grouped by month
    user_counts = db.session.execute(
        """
        SELECT strftime('%Y-%m', date_created) AS month,
        COUNT(id) AS count
        FROM user
        GROUP BY month
        ORDER BY month
        """
    ).fetchall()
    return user_counts



class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    description = db.Column(db.String(500), unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', back_populates='ratings')

    ebook_id = db.Column(db.Integer, db.ForeignKey('ebooks.id', ondelete="CASCADE"), nullable=True)
    ebook = db.relationship('Ebooks', back_populates='ratings')

def get_average_ratings():
    # Subquery to calculate the average rating per book and round it
    subquery = db.session.query(
        Rating.ebook_id,
        func.round(func.avg(Rating.value), 0).label('rounded_rating')
    ).group_by(Rating.ebook_id).subquery()

    # Main query to count the number of books for each rounded average rating
    avg_ratings = db.session.query(
        subquery.c.rounded_rating,
        func.count(subquery.c.ebook_id).label('book_count')
    ).group_by(subquery.c.rounded_rating).all()

    # Convert to a list of dictionaries
    results = [{"rating": int(rounded_rating), "count": book_count} for rounded_rating, book_count in avg_ratings]
    print(results)  # Debug: Print to verify data
    return results

class UsersTime(db.Model):
    __tablename__ = 'UsersTime'
    id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    login_time = db.Column(db.DateTime(timezone=True), default=func.now())
    logout_time = db.Column(db.DateTime(timezone=True))
    ActiveStatus= db.Column(db.Boolean, default=True, nullable=False)