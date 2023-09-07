from flask import url_for
from flask_login import UserMixin


class StudentLogin(UserMixin):

    def is_authenticated(self):
        return True

    def fromDB(self, user_id, db):
        self.__user = db.getStudent(user_id)

        return self

    def createe(self, user):
        self.__user = user
        return self

    def get_id(self):
        if self.__user is not None:
            return str(self.__user['id'])
        return None

    def getName(self):
        return self.__user['name'] if self.__user else "No name"

    def getEmail(self):
        return self.__user['email'] if self.__user else "No email"

    def getLogin(self):
        return self.__user['login'] if self.__user else "No login"

    def getHavebook(self):
        if self.__user is not None:
            return self.__user['have_book'] if self.__user else "No book"
        return None


    def getStat(self):
        if self.__user is not None:
            return self.__user['stat']
        return None

    def getCountlimit(self):
        if self.__user is not None:
            return self.__user['count_limit']
        return None

    def getLimit(self):
        if self.__user is not None:
            return self.__user['limit']
        return None

    def getB_time(self):
        if self.__user is not None:
            return self.__user['b_time']
        return None


    def getFirsttime(self):
        if self.__user is not None:
            return self.__user['time']
        return None

    def getAvatar(self, app):
        img = None

        if self.__user and "avatar" in self.__user and self.__user["avatar"]:
            img = self.__user['avatar']
        else:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='/images/default.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Default avatar not found: " + str(e))

        return img

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == 'png' or ext == "PNG":
            return True
        return False
