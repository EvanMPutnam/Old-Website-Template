from main import db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    content = db.Column(db.Text)
    image = db.Column(db.String(100))


class PortfolioPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    content = db.Column(db.Text)
    image = db.Column(db.String(100))



class LoginForm(FlaskForm):
    '''
    Form data used to log in.
    '''
    userName = StringField('user', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('upload')

class User(UserMixin, db.Model):
    '''
    User data stored in the database
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.Text)
