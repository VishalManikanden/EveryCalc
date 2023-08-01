from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo


class SignUpForm(FlaskForm):
    username = StringField("Username", default="", validators=[InputRequired()])
    password = PasswordField("Password", default="", validators=[InputRequired(), Length(min=8, message="Your password must be a minimum of 8 characters"),
                                                                 EqualTo("confirm_password", message="Password and password confirmation do not match")])
    confirm_password = PasswordField("Confirm password", default="", validators=[InputRequired()])
    submit = SubmitField("Sign up")


class SignInForm(FlaskForm):
    username = StringField("Username", default="", validators=[InputRequired()])
    password = PasswordField("Password", default="", validators=[InputRequired()])
    submit = SubmitField("Sign in")


class SearchForm(FlaskForm):
    search = StringField("Search calculators", validators=[])
    submit = SubmitField("Search")


class ContactForm(FlaskForm):
    name = StringField("Name", default="", validators=[InputRequired()])
    email = EmailField("Email", default="", validators=[InputRequired(), Email(message="Invalid email address")])
    message = TextAreaField("Message", default="", validators=[InputRequired()])
    submit = SubmitField("Contact")

