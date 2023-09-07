from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from data.FDataBase import FDataBase
from data.models.admin_data.admin import User
from data.models.books import Books, BooksCopy
from data.models.students import Students
from form import RegisterForm

# To generate a password for the main admin
# password = ""
# s = generate_password_hash(password)
# print(s)


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)

@admin.route('/')
def index():
    dbase = FDataBase()
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template("admin/index.html", menu1=dbase.getMenu_admin_lower(), menu=dbase.getMenu_admin(),
                           title='Admin Panel', admins=dbase.getAdmins())

@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))

    if request.method == "POST":
        login_input = request.form['user']
        password_input = request.form['psw']
        admin_user = User.select().where(User.login == login_input).first()

        if admin_user and check_password_hash(admin_user.psw, password_input):
            login_admin()
            session['main_admin'] = login_input
            return redirect(url_for('.index'))
        else:
            flash("Incorrect username/password combination", 'error')

    return render_template('admin/login.html', title='Admin Panel')

@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    flash("You have logged out", 'success')
    logout_admin()

    return redirect(url_for('.login'))

@admin.route("/students")
def students():
    dbase = FDataBase()
    if not isLogged():
        flash("Log in to access", 'warning')
        return redirect(url_for('.login'))

    return render_template('admin/index_students.html', menu=dbase.getMenu_admin(), students=dbase.getStudentsAnonce())

@admin.route("/bookscopy")
def booksCopy():
    dbase = FDataBase()
    if not isLogged():
        flash("Log in to access", 'warning')
        return redirect(url_for('.login'))
    return render_template('admin/index_books_copy.html', menu=dbase.getMenu_admin(),
                           copydetail=dbase.getBooksCopyAnonce(), books=dbase.getBooksAnonce())

@admin.route("/regAdmin", methods=["POST", "GET"])
def regAdmin():
    if not isLogged():
        return redirect(url_for('.index'))
    dbase = FDataBase()
    if request.method == "POST":
        login_input = request.form['login']
        password_input = request.form['psw']
        email = request.form['email']
        user_status = request.form['user_status']

        if session.get('main_admin') == "Admin":

            hashed_password = generate_password_hash(password_input)

            User.create(login=login_input, psw=hashed_password, email=email, user_status=user_status)

            flash("Admin successfully registered", 'success')
            return redirect(url_for('.login'))
        else:
            flash("You do not have permission to register administrators", 'error')

    return render_template('admin/register_admin.html', menu=dbase.getMenu_admin(), title='Admin Registration')

@admin.route("/regBook", methods=["POST", "GET"])
def regBook():
    dbase = FDataBase()
    if not isLogged():
        return redirect(url_for('.index'))
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        ISBN = request.form['ISBN']
        genre = request.form['genre']
        url = request.form['url']
        image = request.form['image']
        about = request.form['about']

        if session.get('main_admin') == "Admin":
            Books.create(
                title=title,
                authors=author,
                year=year,
                ISBN=ISBN,
                genre=genre,
                url=url,
                image=image,
                about=about
            )
            flash("Book successfully registered", 'success')
            return redirect(url_for('.index'))
        else:
            flash("You do not have permission to register books", 'error')

    return render_template('admin/register_book.html', menu=dbase.getMenu_admin(), title='Book Registration')

@admin.route("/regBookCopy", methods=["POST", "GET"])
def regBookCopy():
    if not isLogged():
        return redirect(url_for('.index'))
    dbase = FDataBase()
    if request.method == "POST":
        book_id = request.form['book_id']
        state = request.form['state']

        if session.get('main_admin') == "Admin":
            try:
                new_copy = BooksCopy.create(
                    book_id=book_id,
                    state=state)

                if new_copy:
                    flash("Book copy successfully registered", 'success')
                    return redirect(url_for('.index'))
                else:
                    flash("Error registering book copy", 'error')
            except Exception as e:
                flash(f"Error registering book copy: {str(e)}", 'error')
        else:
            flash("You do not have permission to register book copies", 'error')

    return render_template('admin/register_bookcopy.html', menu=dbase.getMenu_admin(), title='Book Copy Registration')

@admin.route("/abooks", methods=["POST", "GET"])
def aBooks():
    dbase = FDataBase()
    return render_template('admin/index_abooks.html', menu=dbase.getMenu_admin(), menu1=dbase.getMenu_admin_lower(),
                           books=dbase.getBooksAnonce())


@admin.route("/abooks/<alias>", methods=["GET", "POST"])
def showaBook(alias):
    dbase = FDataBase()
    book_data = dbase.getBooks(alias)

    if not book_data:
        abort(404)

    book = Books(**book_data)

    if request.method == "POST":
        if "delete" in request.form:
            dbase.deleteColumn(Books, book.url)
            flash("Book successfully deleted", "success")
            return redirect(url_for('.index'))

        book.title = request.form.get("title")
        book.authors = request.form.get("authors")
        book.year = request.form.get("year")
        book.ISBN = request.form.get("ISBN")
        book.genre = request.form.get("genre")
        book.about = request.form.get("about")
        dbase.updateBook(book)
        if dbase.updateBook(book):
            flash("Book data successfully updated", "success")
            return redirect(url_for('.index'))
        else:
            flash("Error updating book data", "error")
            return redirect(url_for('.index'))

    return render_template('admin/abooks.html', menu=dbase.getMenu_admin(), menu1=dbase.getMenu_admin_lower(),
                           books=book)


@admin.route("/students/<alias>", methods=["GET", "POST"])
def showStudents(alias):
    dbase = FDataBase()
    if not isLogged():
        return redirect(url_for('.index'))

    student_data = dbase.getStudent_url(alias)
    if not student_data:
        abort(404)

    student = Students(**student_data)

    if request.method == "POST":
        if "delete" in request.form:
            dbase.deleteColumn(Students, student.url)
            flash("Student successfully deleted", "success")
            return redirect(url_for('.index'))

        student.fullname = request.form.get("fullname")
        student.email = request.form.get("email")
        student.login = request.form.get("login")

        if "have_book" in request.form:
            student.have_book = request.form.get("have_book")
        else:
            student.have_book = None

        student.count_limit = request.form.get("count_limit")
        student.limit = request.form.get("limit")
        b_time_input = request.form.get("b_time")
        student.b_time = None if b_time_input == "None" else b_time_input
        student.time = request.form.get("time")
        dbase.updateStudent(student)

        if dbase.updateStudent(student):
            flash("Student data successfully updated", "success")
        else:
            flash("Error updating student data", "error")
        return redirect(url_for('.index'))

    return render_template('admin/students.html', menu=dbase.getMenu_admin(), menu1=dbase.getMenu_admin_lower(),
                           students=student)

@admin.route("/bookscopy/<alias_id>", methods=['GET', 'POST'])
def showBooksCopy(alias_id):
    dbase = FDataBase()

    bookcopy = dbase.get_book_copies_by_book_id(alias_id)

    if not bookcopy:
        abort(404)

    if request.method == "POST":
        if "delete" in request.form:
            book_copy_id_delete = request.form.get('id')
            if dbase.deleteColumn(BooksCopy, book_copy_id_delete):
                flash("Book copy successfully deleted", "success")
            else:
                flash("Error deleting book copy", "error")
                return redirect(url_for('.index'))
        else:
            book_copy_id_update = request.form.get('id')
            bookcopy = dbase.get_book_copy_by_id(book_copy_id_update)
            if bookcopy is not None:
                bookcopy.state = request.form.get('state')
                bookcopy.status = request.form.get('status')
                if dbase.updateCopyData(bookcopy):
                    flash("Book copy data updated successfully", "success")
                else:
                    flash("Error updating book copy data", "error")
        return redirect(url_for('.index'))

    return render_template("admin/bookcopys.html", menu=dbase.getMenu_admin(), bookcopies=bookcopy,
                           book=dbase.getBookById(alias_id))


@admin.route("/regStud", methods=["POST", "GET"])
def regStud():
    if not isLogged():
        return redirect(url_for('.index'))
    dbase = FDataBase()
    form = RegisterForm()
    if form.validate_on_submit():

        data = {
            'fullname': form.name.data,
            'login': form.login.data,
            'email': form.email.data,
            'psw': generate_password_hash(form.psw.data),
            'url': form.name.data.replace(" ", "_"),
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        res = Students.create(**data)

        if res:
            flash("You have successfully registered a student", "success")
            return redirect(url_for('.login'))
        else:
            flash("Error adding to the database", "error")

    return render_template('admin/register.html', menu=dbase.getMenu_admin(), menu1=dbase.getMenu_admin_lower(),
                           title="Registration", form=form)


@admin.route('/search_student', methods=['GET', 'POST'])
def search_student():
    dbase = FDataBase()
    if request.method == 'POST':
        search_input = request.form['search_student']

        if search_input.isdigit():
            posts = Students.select().where(Students.id == int(search_input))
        else:
            posts = Students.select().where(Students.fullname.contains(search_input))
    else:
        posts = Students.select()

    return render_template('admin/search_student.html', posts=posts, menu=dbase.getMenu_admin(),
                           students=dbase.getStudentsAnonce())


@admin.route('/search_book_A', methods=['GET', 'POST'])
def search_Book_A():
    dbase = FDataBase()
    if request.method == 'POST':
        search_input = request.form['search_book_A']

        if search_input.isdigit():
            posts = Books.select().where(Books.id == int(search_input))
        else:
            posts = Books.select().where(Books.title.contains(search_input))
    else:
        posts = Books.select()

    return render_template('admin/search_book_A.html', posts=posts, menu=dbase.getMenu_admin(),
                           books=dbase.getBooksAnonce())


@admin.route('/search_bookcopy_A', methods=['GET', 'POST'])
def search_Bookcopy_A():
    dbase = FDataBase()
    if request.method == 'POST':
        search_input = request.form['search_bookcopy_A']

        if search_input.isdigit():
            posts = Books.select().where(Books.id == int(search_input))
        else:
            posts = Books.select().where(Books.title.contains(search_input))
    else:
        posts = Books.select()

    return render_template('admin/search_bookcopy_A.html', posts=posts, menu=dbase.getMenu_admin(),
                           books=dbase.getBooksAnonce())


@admin.errorhandler(404)
def not_found(error):
    dbase = FDataBase()
    return render_template('admin/error.html', menu=dbase.getMenu_admin()), 404