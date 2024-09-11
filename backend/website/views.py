from datetime import datetime, timedelta
from email.charset import BASE64
from flask import Blueprint, jsonify,render_template
import base64
from flask_jwt_extended import create_access_token, get_jwt,jwt_required,get_jwt_identity
from sqlalchemy import func, text
# from .task import add, create_csv
from celery.result import AsyncResult
from . import db
from . import cache

from .models import Admin, Ebooks, Rating, Section, User,Request,UsersTime, get_average_ratings, get_request_counts_by_genre, user_growth
views = Blueprint('views', __name__)

# Define a unique route for the home page
# @views.route('/')
# @views.route('/home', methods=["GET"])
# def home():
#     return "home books and rows"


# @views.route("/start-export")
# def start_export():
#     task = create_csv.delay()
#     return jsonify({"task_id": task.id})



# @views.route('/celerydemo')
# def celery_demo():
#     task= add.delay(10,30)
#     return jsonify({'task_id':task.id})

# Define a unique route for the login page

@views.route('/getvalue/<id>')
def get_task(id):
    result = AsyncResult(id)
    print(result)

    if result.ready():
        return jsonify({"result": result.result})
    else:
        return "task not ready", 405


@views.route('/api/dashboard', methods=["GET"])
@jwt_required()
@cache.cached(timeout=60, query_string=True)
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    user_data = []
    if user:
        profile_image_base64 = base64.b64encode(user.profile_image).decode('utf-8') if user.profile_image else None
        user_data = {
            "id":user.id,
            "username": user.username,
            "profile_image": profile_image_base64,  # Assuming you handle image conversion elsewhere
        }
    print(user)
    return jsonify({"user": user_data})


@views.route('/api/adminDashboard', methods=["GET"])
@views.route('/api/AllUsers', methods=["GET"])
@jwt_required()
@cache.cached(timeout=60, query_string=True)
def adminDashboard():

    current_user_email = get_jwt_identity()
    if current_user_email != "admin":
        return jsonify({"message": "Unauthorized access"}), 403

    users = User.query.all()
    user_count = User.query.count()
    Book_count = Ebooks.query.count()
    Section_count = Section.query.count()


    # Get the most recent login and logout times for each user
    user_status = {}
    for user_time in db.session.query(
        UsersTime.UserId,
        UsersTime.login_time,
        UsersTime.logout_time
    ).order_by(UsersTime.UserId, UsersTime.login_time.desc()).all():
        user_id = user_time.UserId
        if user_id not in user_status:
            user_status[user_id] = user_time
    # print(user_status)

    # Prepare user data with the login status information
    users_data = []
    for user in users:
        profile_image_base64 = base64.b64encode(user.profile_image).decode('utf-8') if user.profile_image else None
        status = user_status.get(user.id)
        last_login_time = status.login_time if status else None

        # Determine if the user is logged in based on the login and logout times
        is_logged_in = status and status.logout_time is None
        users_data.append({
            "id": user.id,
            "username": user.username,
            "profile_image": profile_image_base64,
            'book_count':user.book_count,
            "is_logged_in": is_logged_in,
            "last_login_time": last_login_time,
        })

    return jsonify({"users": users_data,"User_count":user_count,"Book_count":Book_count,"Section_count":Section_count})


@views.route('/api/ebooksDashboard', methods=["GET"])
@views.route('/api/AllBooks', methods=["GET"])
@cache.cached(timeout=60, query_string=True)
@jwt_required()
def ebooksDashboard():
    ebooks = Ebooks.query.all()
    ebooks_data = []

    # Compute average rating for each book
    for ebook in ebooks:
        ratings = Rating.query.filter_by(ebook_id=ebook.id).all()
        if not ratings:
            average_rating = 0
        else:
            total_rating = sum([rating.value for rating in ratings])
            average_rating = total_rating / len(ratings)

        profile_image_base64 = base64.b64encode(ebook.Book_profile_image).decode('utf-8') if ebook.Book_profile_image else None
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
            "average_rating": average_rating
        })

    # Sort books by average rating in descending order
    ebooks_data_sorted = sorted(ebooks_data, key=lambda x: x['average_rating'], reverse=True)

    return jsonify({"ebooks": ebooks_data_sorted})

# In your Flask route
@views.route('/api/request_counts', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, query_string=True)
def request_counts():
    # Define a dictionary to hold the count for each genre
    genre_counts = {
        "Adventure": 0,
        "Fantasy": 0,
        "Historical": 0,
        "Horror": 0,
        "Mystery": 0,
        "Romance": 0,
        "Thriller": 0,
        "Biography": 0,
        "Non-Fiction": 0,
        "Drama": 0
    }
    # Retrieve the data from the database
    results = get_request_counts_by_genre()

    # Iterate over the results
    for result in results:
        genres = result[0].split(',')  # Split the genre string into individual genres
        count = result[1]

        # Increment the count for each genre found in the list
        for genre in genres:
            genre = genre.strip()  # Remove any leading/trailing spaces
            if genre in genre_counts:
                genre_counts[genre] += count

    # Convert the dictionary to a list of dictionaries for JSON response
    data = [{"genre": genre, "count": count} for genre, count in genre_counts.items()]
    return jsonify(data)

@views.route('/api/user_growth', methods=['GET'])
@jwt_required()
def user_growth():
    sql = text("""
        SELECT strftime('%Y-%m-%d', date_created) AS day,
        COUNT(id) AS count
        FROM user
        GROUP BY day
        ORDER BY day
    """)
    user_counts = db.session.execute(sql).fetchall()

    # Prepare the data for the frontend
    data = [
        {"day": day, "count": count}
        for day, count in user_counts
    ]
    print(data)
    return jsonify(data)

@views.route('/api/average_ratings', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, query_string=True)
def average_ratings():
    # Subquery to calculate average rating per book and round it
    data = get_average_ratings()
    print(data)
    return jsonify(data)
