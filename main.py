from flask import Flask, render_template, abort, redirect, url_for, request, flash, Response
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from peewee import PostgresqlDatabase
import datetime
from UserLogin import StudentLogin
from data.db import CONNECTION_STRING
from data.FDataBase import FDataBase
from werkzeug.security import check_password_hash
from data.models.books import Books
from data.models.students import Students
from form import LoginForm
from admin.admin import admin


app = Flask(__name__)
app.config["SECRET_KEY"] = "fasseffawfawfgarwegaer"

app.register_blueprint(admin, url_prefix='/admin')

db = PostgresqlDatabase(CONNECTION_STRING)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Log in to access restricted pages"
login_manager.login_message_category = 'success'


@app.context_processor
def inject_helpers():
    return dict(time_now=time_now)


@login_manager.user_loader
def load_student(user_id):
    dbase = FDataBase()
    return StudentLogin().fromDB(user_id, dbase)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    dbase = FDataBase()
    form = LoginForm()
    if form.validate_on_submit():

        student = dbase.getstudentByLogin(form.login.data)

        if student and check_password_hash(student['psw'], form.psw.data):
            studentlogin = StudentLogin().createe(student)
            rm = form.remember.data
            login_user(studentlogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))
        flash("Invalid username/password", "error")
        print(current_user)
    return render_template('login.html', menu=dbase.getMenu(), title="Authorization", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out", "success")
    return redirect(url_for('login'))


@app.route("/profile")
@login_required
def profile():
    dbase = FDataBase()
    list_book = []
    havebook = current_user.getHavebook()
    if havebook is not None:
        for book_id in havebook:
            list_book.append(dbase.getBookById(int(book_id)))
    return render_template("profile.html", menu=dbase.getMenu(), title="Profile", list_title=list_book,
                           books=dbase.getBooksAnonce())


@app.route("/userava")
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""

    response = Response(img, content_type='image/png')
    return response


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    dbase = FDataBase()
    if request.method == "POST":
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash("Avatar update error", "error")
                flash("Avatar updated", "success")
            except FileNotFoundError as e:
                flash("File read error", "error")
        else:
            flash("Avatar update error", "error")

    return redirect(url_for("profile"))


@app.route("/")
def index():
    dbase = FDataBase()
    return render_template('index.html', menu=dbase.getMenu(), books=dbase.getBooksAnonce())


@app.route("/book/<alias>", methods=['GET', 'POST'])
def showBook(alias):
    dbase = FDataBase()
    books = dbase.getBooks(alias)
    bookcopy = dbase.getBooksCopyAnonce()
    student_id = current_user.get_id()
    student = Students.get_or_none(id=student_id)
    if current_user.is_authenticated:
        copy_havebook = current_user.getHavebook()
    else:
        copy_havebook = None

    if copy_havebook is None:
        copy_havebook = []


    if books is None:
        abort(404)

    if copy_havebook is None:
        copy_havebook = []

    if request.method == "POST":
        if "reserve_book" in request.form and current_user.get_id():
            if current_user.getStat() == 1:
                flash("Your decency is equal to 1, contact the Admin", 'error')
            else:
                reserved_copy = None
                for copy in bookcopy:
                    if copy.status == "Free" and copy.book_id == books['id']:
                        reserved_copy = copy
                        break

                if reserved_copy is not None and student.count_limit < student.limit and str(reserved_copy.book_id) not in copy_havebook:
                    if reserved_copy.reserve():
                        Students.update_student_data(student_id, books['id'])
                        flash("You have successfully booked the book, you have 14 days to return the book", 'success')
                else:
                    flash("Sorry, this book is not available", 'error')
                if student.count_limit >= 5:
                    flash("You have the maximum number of books", 'error')

        elif "return_book" in request.form:
            reserved_copy = None
            for copy in bookcopy:
                if copy.status == "Busy" and copy.book_id == books['id'] and str(copy.book_id) in current_user.getHavebook():
                    reserved_copy = copy
                    break

            if reserved_copy is not None:
                if reserved_copy.reserve_back():
                    Students. remove_student_data(student_id, books['id'])
                    flash("You have successfully returned the book!", 'success')
            else:
                flash("You don't have this book!", 'error')
        else:
            return redirect(url_for('login'))

    return render_template('books.html', menu=dbase.getMenu(), books=books, bookcopy=bookcopy)


@app.route("/about_us")
def aboutUs():
    dbase = FDataBase()
    return render_template('about_us.html', menu=dbase.getMenu())


def time_now():
    current_time = datetime.datetime.now()
    return f"Date and Time: {current_time.replace(second=0, microsecond=0)}"


@app.route('/search_book', methods=['GET', 'POST'])
def search_book():
    dbase = FDataBase()
    if request.method == 'POST':
        search_book = request.form['search_book']
        posts = Books.select().where(Books.title.contains(search_book))
    else:
        posts = Books.select()
    return render_template('search_book.html', posts=posts, menu=dbase.getMenu(),books=dbase.getBooksAnonce())


@app.errorhandler(404)
def not_found(error):
    dbase = FDataBase()
    return render_template('error.html', menu=dbase.getMenu()), 404

if __name__ == "__main__":
    app.run(debug=True)


