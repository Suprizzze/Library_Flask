from datetime import datetime

from flask import flash
from peewee import *
from playhouse.postgres_ext import ArrayField

from data.db import db


class Students(Model):
    id = AutoField(primary_key=True, null=False)
    fullname = CharField(null=False)
    email = CharField(null=False)
    login = TextField(null=False)
    psw = TextField(null=False)
    avatar = BlobField(null=True)
    have_book = ArrayField(CharField, null=True)
    stat = IntegerField(default=10, null=True)
    count_limit = IntegerField(default=0, null=True)
    limit = IntegerField(default=5, null=True)
    b_time = ArrayField(CharField, default=None, null=True)
    url = TextField(null=False)
    time = TextField(null=False)

    @classmethod
    def update_student_data(cls, student_id, book_id):
        try:
            student = cls.get(id=student_id)
            if student:
                current_date = datetime.now().date()

                existing_b_time = student.b_time or []
                existing_have_book = student.have_book or []

                existing_b_time.append(current_date)

                if book_id:
                    existing_have_book.append(book_id)

                student.b_time = existing_b_time
                student.have_book = existing_have_book
                student.count_limit += 1

                student.save()
                print("Student data updated successfully")
                return True
            else:
                print("Student not found")
                return False
        except cls.DoesNotExist:
            print(f"Student with id {student_id} does not exist")
            return False

    @classmethod
    def remove_student_data(cls, student_id, book_id):
        try:
            student = cls.get(id=student_id)
            current_date = datetime.now().date()
            if student:
                index_to_remove = None
                book_id_to_remove = None

                for i, book_time in enumerate(student.b_time):
                    if student.have_book[i] == str(book_id):
                        index_to_remove = i
                        book_id_to_remove = student.have_book[i]
                        break

                if index_to_remove is not None:

                    b_time_str = student.b_time[index_to_remove]

                    b_time = datetime.strptime(b_time_str, "%Y-%m-%d").date()

                    time_difference_in_seconds = (current_date - b_time).total_seconds()
                    print(time_difference_in_seconds)
                    if time_difference_in_seconds > (14 * 24 * 60 * 60):
                        flash("You returned a book more than 14 days late", 'error')

                        student.stat = 1
                        student.save()

                    student.b_time.pop(index_to_remove)

                    if book_id_to_remove is not None:
                        student.have_book.remove(book_id_to_remove)

                    student.count_limit -= 1

                    student.save()
                    print("Student data updated successfully")
                    return True
                else:
                    print("The book with the specified book_id was not found in the student's have_book list")
                    return False
            else:
                print("Student not found")
                return False

        except cls.DoesNotExist:
            print(f"The student with id {student_id} does not exist")
            return False

    class Meta:
        database = db


if __name__ == "__main__":
    db.create_tables([Students])
