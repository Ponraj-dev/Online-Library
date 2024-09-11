import csv
from datetime import datetime
from celery.result import AsyncResult
import os
from celery import Celery,shared_task
import flask_excel as excel
from celery.schedules import crontab
from jinja2 import Template
from sqlalchemy import extract, func
from .email import send_email
from . import db
from flask import Blueprint, current_app, jsonify
from .models import Ebooks, Rating, Request, Section, User

celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

report_bp = Blueprint('report', __name__)

@celery.task()
def export_csv_report():
     with current_app.app_context():
          requests = db.session.query(Request, Ebooks).join(Ebooks, Request.ebook_id == Ebooks.id).all()

          timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
          report_filename = f"ebook_report_{timestamp}.csv"

          # Ensure the directory exists
          output_directory = './book_reports'
          os.makedirs(output_directory, exist_ok=True)
          output_path = os.path.join(output_directory, report_filename)

          # Write the data to the CSV file
          with open(output_path, "w", newline='') as file:
               writer = csv.writer(file)
               writer.writerow(["Name", "Authors", "description","Date Issued", "Return Date"])
               for request, ebook in requests:
                    writer.writerow([
                         ebook.bookname,
                         ebook.Authors,
                         ebook.description,
                         request.approved_date.strftime("%Y-%m-%d") if request.approved_date else "N/A",
                         request.due_date.strftime("%Y-%m-%d") if request.due_date else "N/A"
                    ])

          return output_path


@shared_task(ignore_result = True)
def daily_reminder(to,sub,message):
     send_email(to,sub,message)
     return "ok"

@shared_task(ignore_result = True)
def send_daily_mail():
     template_str = """
<p>Hey {{ name }},</p>
<br />
<p>It's your favorite librarian here, and I've got a burning question: Where have you been? The books are getting lonely without you, and I'm pretty sure they started a book club just to gossip about your absence!</p>
<p>Try to login and check up status of your learning.</p>
<br />
<p>Your Friendly Librarian</p>
<p>Regards</p>
"""
     template = Template(template_str)
     print("Task started: Sending daily emails")



     with db.session() as session:
          all_users = session.query(User).all()
          current_date = datetime.utcnow().date()
          print("Current date:", current_date)

          for user in all_users:
               if user.login_time:
                    login_check = user.login_time.date()
                    print(f"User {user.username} login time: {user.login_time}, date part: {login_check}")
               else:
                    login_check = None
                    print(f"User {user.username} has no login time recorded")

               if login_check != current_date:
                    print(f"user: {user.username} has not logged in today")
                    body = template.render(name=user.username)
                    subject = 'Please Log In Today'
                    print("code trying")
                    send_email(user.email, subject, body)
                    print("code runs")
               else:
                    print(f"user: {user.username} has logged in today")

     print("Task completed: Daily emails sent")
     return 200

@shared_task(ignore_result=True)
def send_monthly_report():
     adminEmail = 'ponrajofficial19@gmail.com'
     template_str = '''
     <p>Hello Librarian,</p>
     <br>
     <h3>📚 Monthly Library Report 📚</h3>
     <br>
     {% if booksCreated|length > 0 %}
          <h4>📘 New Books Added</h4>
          <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
               <thead>
                    <tr>
                         <th>ID</th>
                         <th>Book Name</th>
                         <th>Author</th>
                         <th>Genres</th>
                         <th>Date Added</th>
                    </tr>
               </thead>
               <tbody>
                    {% for book in booksCreated %}
                    <tr>
                         <td>{{ book.id }}</td>
                         <td>{{ book.bookname }}</td>
                         <td>{{ book.Authors }}</td>
                         <td>{{ book.genre }}</td>
                         <td>{{ book.date_issued.strftime('%Y-%m-%d') }}</td>
                    </tr>
                    {% endfor %}
               </tbody>
          </table>
     {% else %}
          <p>No new books were added this month.</p>
     {% endif %}
     <br>
     {% if sectionsCreated|length > 0 %}
          <h4>📚 New Sections Created</h4>
          <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
               <thead>
                    <tr>
                         <th>ID</th>
                         <th>Section Name</th>
                         <th>Genre</th>
                         <th>Date Created</th>
                    </tr>
               </thead>
               <tbody>
                    {% for sec in sectionsCreated %}
                    <tr>
                         <td>{{ sec.id }}</td>
                         <td>{{ sec.name }}</td>
                         <td>{{ sec.genre }}</td>
                         <td>{{ sec.date_created.strftime('%Y-%m-%d') }}</td>
                    </tr>
                    {% endfor %}
               </tbody>
          </table>
     {% else %}
          <p>No new sections were created this month.</p>
     {% endif %}
     <br>
     {% if booksIssuedCreated|length > 0 %}
          <h4>📖 Books Issued</h4>
          <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
               <thead>
                    <tr>
                         <th>ID</th>
                         <th>Book Name</th>
                         <th>User ID</th>
                         <th>User Name</th>
                    </tr>
               </thead>
               <tbody>
                    {% for book in booksIssuedCreated %}
                    <tr>
                         <td>{{ book.Bid }}</td>
                         <td>{{ book.BName }}</td>
                         <td>{{ book.Uid }}</td>
                         <td>{{ book.UName }}</td>
                    </tr>
                    {% endfor %}
               </tbody>
          </table>
     {% else %}
          <p>No books were issued this month.</p>
     {% endif %}
     <br>
     {% if booksRatingCreated|length > 0 %}
          <h4>⭐ Book Ratings</h4>
          <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
               <thead>
                    <tr>
                         <th>ID</th>
                         <th>Book Name</th>
                         <th>User ID</th>
                         <th>User Name</th>
                         <th>Rating</th>
                    </tr>
               </thead>
               <tbody>
                    {% for rating in booksRatingCreated %}
                    <tr>
                         <td>{{ rating.Book_id }}</td>
                         <td>{{ rating.Book_name }}</td>
                         <td>{{ rating.Uid }}</td>
                         <td>{{ rating.UName }}</td>
                         <td>{{ rating.rating }}</td>
                    </tr>
                    {% endfor %}
               </tbody>
          </table>
     {% else %}
          <p>No ratings were given this month.</p>
     {% endif %}
     <br>
     <p>That's all for this month! Keep up the great work and happy reading!</p>
     <br>
     <p>Best Regards,</p>
     <p>Your Library Team</p>
     '''

     template = Template(template_str)
     current_date = datetime.now()

     with db.session() as session:
          # Books Created
          booksCreated = session.query(Ebooks).filter(
               extract('month', Ebooks.date_issued) == current_date.month
          ).all()

          # Sections Created
          sectionsCreated = session.query(Section).filter(
               extract('month', Section.date_created) == current_date.month
          ).all()

          # Books Issued
          booksIssuedCreated = []
          for request in session.query(Request).filter(
               extract('month', Request.request_date) == current_date.month
          ).all():
               user = session.query(User).filter_by(id=request.user_id).first()
               book = session.query(Ebooks).filter_by(id=request.ebook_id).first()
               booksIssuedCreated.append({
                    'Bid': book.id,
                    'BName': book.bookname,
                    'Uid': user.id,
                    'UName': user.username
               })

          # Book Ratings
          booksRatingCreated = []
          # for rating in session.query(Rating).filter(
          #      extract('month', Rating.date_created) == current_date.month
          # ).all():
          #      user = session.query(User).filter_by(id=rating.user_id).first()
          #      book = session.query(Ebooks).filter_by(id=rating.ebook_id).first()
          #      booksRatingCreated.append({
          #           'Uid': user.id,
          #           'UName': user.username,
          #           'Book_id': book.id,
          #           'Book_name': book.bookname,
          #           'rating': rating.value
          #      })

          body = template.render(
               booksCreated=booksCreated,
               sectionsCreated=sectionsCreated,
               booksIssuedCreated=booksIssuedCreated,
               booksRatingCreated=booksRatingCreated
          )
          subject = 'Monthly Library Report'
          send_email(adminEmail, subject, body)

     return 200


@report_bp.route('/api/trigger_report', methods=['POST'])
def trigger_report():
     task = export_csv_report.delay()
     return jsonify({"task_id": task.id}), 202

