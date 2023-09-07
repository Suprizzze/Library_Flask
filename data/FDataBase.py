from data.models.admin_data.admin import User
from data.models.mainmenu import Mainmenu, Mainmenu_admin, Mainmenu_admin_lower
from data.models.books import Books, BooksCopy
from data.models.students import Students


class FDataBase:

    def getMenu(self):
        try:
            menu_items = Mainmenu.select().order_by(Mainmenu.id)
            return [{"title": item.title, "url": item.url} for item in menu_items]
        except Exception as e:
            print(f"Error reading from DB: {e}")
            return []

    def getMenu_admin(self):
        try:
            menu_items = Mainmenu_admin.select().order_by(Mainmenu_admin.id)
            return [{"title": item.title, "url": item.url} for item in menu_items]
        except Exception as e:
            print(f"Error reading from DB:: {e}")
            return []

    def getMenu_admin_lower(self):
        try:
            menu_items = Mainmenu_admin_lower.select().order_by(Mainmenu_admin_lower.id)
            return [{"title": item.title, "url": item.url} for item in menu_items]
        except Exception as e:
            print(f"Error reading from DB:: {e}")
            return []


    def getBooks(self, alias):
        try:
            book_instance = Books.get_or_none(url=alias)
            if book_instance:
                book_data = {
                    "id": book_instance.id,
                    "title": book_instance.title,
                    "authors": book_instance.authors,
                    "year": book_instance.year,
                    "ISBN": book_instance.ISBN,
                    "genre": book_instance.genre,
                    "url": book_instance.url,
                    "image": book_instance.image,
                    "about": book_instance.about
                }
                return book_data
        except Exception as e:
            print("Error getting book from database: " + str(e))

        return None

    def get_book_copies_by_book_id(self, book_id):
        book_copies = BooksCopy.select().where(BooksCopy.book_id == book_id)
        return book_copies

    def getStudent_url(self, alias):
        try:
            students = Students.get_or_none(url=alias)
            if students:
                student_data = {
                    "id": students.id,
                    "fullname": students.fullname,
                    "email": students.email,
                    "login": students.login,
                    "have_book" : students.have_book,
                    "stat": students.stat,
                    "limit": students.limit,
                    "count_limit": students.count_limit,
                    "b_time": students.b_time,
                    "url": students.url,
                    "time": students.time
                }
                return student_data
        except Exception as e:
            print("Error getting student from database: " + str(e))

        return None

    def updateCopyData(self, book_copy):
        try:
            bookcopy = BooksCopy.get_or_none(id=book_copy.id)
            if book_copy:
                bookcopy.id = book_copy.id
                bookcopy.state =book_copy.state
                bookcopy.status = book_copy.status
                bookcopy.save()
                return True
            else:
                print("Record not found in database")
        except Exception as e:
            print("Error updating book copy in database: ", str(e))
        return False

    def updateBook(self, book):
        try:
            book_instance = Books.get_or_none(url=book.url)
            if book_instance:
                book_instance.title = book.title
                book_instance.authors = book.authors
                book_instance.year = book.year
                book_instance.ISBN = book.ISBN
                book_instance.genre = book.genre
                book_instance.about = book.about
                book_instance.save()
                return True
            else:
                print("Record not found in database")
        except Exception as e:
            print("Book database update error: ", str(e))
        return False

    def updateStudent(self, student):
        try:
            student_instance = Students.get_or_none(url=student.url)
            if student_instance:
                student_instance = Students.get_by_id(student.id)
                student_instance.fullname = student.fullname
                student_instance.email = student.email
                student_instance.login = student.login

                if student.have_book is not None:
                    have_book_list = [str(book_id.strip()) for book_id in student.have_book.split(',') if
                                      book_id.strip().isdigit()]
                    student_instance.have_book = have_book_list

                student_instance.count_limit = student.count_limit
                student_instance.limit = student.limit

                if student.b_time is not None:
                    b_time_list = [str(book_id.strip()) for book_id in student.b_time.split(',') if
                                   book_id.strip().isdigit()]
                    student_instance.b_time = b_time_list

                student_instance.url = student.url
                student_instance.time = student.time
                student_instance.save()
                return True
            else:
                print("Запись не найдена в базе данных")
        except Exception as e:
            print("Ошибка при обновлении данных о студенте в базе данных: ", str(e))
        return False

    def deleteColumn(self, table, item):
        try:
            if item.isdigit():
                subject = table.get_by_id(item)
                subject.delete_instance()
                print("Deletion successful")
                return True
            else:
                subject = table.get(table.url == item)
                subject.delete_instance()
                print("Deletion successful")
                return True
        except Exception as e:
            print("Error when deleting a student: " + str(e))
            return False

    def get_book_copy_by_id(self, copy_id):
        try:
            book_copy = BooksCopy.get(BooksCopy.id == copy_id)
            return book_copy
        except BooksCopy.DoesNotExist:
            return None

    def getBooksAnonce(self):
        try:
            books = Books.select(Books).order_by(Books.title)
            return list(books)
        except Exception as e:
            print("Error getting books from database: " + str(e))
            return []

    def getBooksCopyAnonce(self):
        try:
            bookscopies = BooksCopy.select(BooksCopy)
            return list(bookscopies)
        except Exception as e:
            print("Error getting a copy of books from the database: " + str(e))
            return []

    def getStudentsAnonce(self):
        try:
            students = Students.select(Students)
            return list(students)
        except Exception as e:
            print("Error getting students from database: " + str(e))

        return []

    def getStudent(self, student_id):
        try:
            students = Students.get_or_none(id=student_id)
            if students:
                return {
                    "id": students.id,
                    "name": students.fullname,
                    "login": students.login,
                    "email": students.email,
                    "avatar": students.avatar,
                    "stat": students.stat,
                    "limit": students.limit,
                    "count_limit": students.count_limit,
                    "have_book": students.have_book,
                    "b_time": students.b_time,
                    "time": students.time.split(" ")[0]
                }

        except Exception as e:
            print("Error getting students from database: " + str(e))

        return None

    def getBookById(self, book_id):
        try:
            book = Books.get_by_id(book_id)
            return book
        except Books.DoesNotExist:
            return None

    def getstudentByLogin(self, login):
        try:
            student = Students.get_or_none(login=login)
            if student:
                return {
                    "id": student.id,
                    "login": student.login,
                    "psw": student.psw
                }
        except Exception as e:
            print(f"Error reading from DB: {e}")

        return None

    def updateUserAvatar(self, avatar, user_id):
        try:
            student = Students.get_or_none(id=user_id)
            if student:
                student.avatar = bytes(avatar)
                student.save()
                return True
            else:
                return False
        except Exception as e:
            print("Error updating the avatar in the database: " + str(e))
            return False

    def getAdmins(self):
        try:
            admins = User.select()
            admin_list = []
            for admin in admins:
                admin_list.append({
                    "id": admin.id,
                    "login": admin.login,
                    "email": admin.email,
                    "user_status": admin.user_status
                })
            return admin_list
        except Exception as e:
            print("Error getting administrators from database: " + str(e))
            return []

    def is_book_available(self, books_id, bookcopy_list):
        for bookcopy in bookcopy_list:
            if books_id == bookcopy.book_id and bookcopy.status == "Free":
                return True
        return False

