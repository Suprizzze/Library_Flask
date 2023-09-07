from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    login = StringField("Login:ㅤ", validators=[DataRequired(), Length(min=4, max=20, message="Login must be between 4 and 20 characters")])
    psw = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=100, message="Password must be between 4 and 100 characters")])
    remember = BooleanField("Remember", default=False)
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    name = StringField("Name:",validators=[Length(min=4, max=100, message="Name must be between 4 and 100 characters")])
    login = StringField("Login:",validators=[Length(min=4, max=25, message="Login must be between 4 and 25 characters")])
    email = StringField("Email:", validators=[Email("Invalid email")])
    psw = PasswordField("Password:", validators=[DataRequired(), Length(min=4, max=100,
                                                            message="Password must be between 4 and 100 characters")])
    psw2 = PasswordField("Password repeat: ", validators=[DataRequired(), EqualTo('psw',
                                                                       message="Password mismatch")])
    submit = SubmitField("Register")