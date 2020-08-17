from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import date, datetime
import tempfile, os
import firebase

today = date.today()
date = today.strftime("%d/%m/%Y")

now = datetime.now()
time = now.strftime("%H : %M :%S")

###### Registration form

class RegisterForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired(), Email(),])
    password = PasswordField('Password', validators = [DataRequired(),])
    confirm_password = PasswordField('Confirm password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Log In')
###### Login form

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email(),])
    password = PasswordField('Password', validators = [DataRequired(),])
    submit = SubmitField('Log In')

########## Upload a post
class PostForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(min=2)])
    description = TextAreaField('description', validators = [DataRequired(), Length(min=2)])
    picture = FileField("Choose file", validators=[FileAllowed(['jpg', 'png', 'mp4'])])
    submit = SubmitField('Submit')
    post_date = date
    post_time = time
  
    
    

##########   Upload university  
class UniversityForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(), Length(min=2, max=20)])
    country = StringField('Country', validators = [DataRequired(), Length(min=2),])
    description = TextAreaField('Description', validators = [DataRequired(), Length(min=50),])
    majors = TextAreaField('Majors', validators = [DataRequired(), Length(min=50),])
    logo = PasswordField('Confirm password', validators = [DataRequired(), EqualTo('password')])
    web = StringField('Web url', validators = [DataRequired(), Length(min=2)])
    deadline = StringField('Deadline', validators = [DataRequired(), Length(min=2)])     
    submit = SubmitField('Submit')

##########  Upload Scholarship     
class ScholarshipForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(), Length(min=2, max=20)])
    country = StringField('Country', validators = [DataRequired(), Length(min=2),])
    description = TextAreaField('Description', validators = [DataRequired(), Length(min=50),])
    advantage = TextAreaField('Advantages', validators = [DataRequired(), Length(min=50),])
    logo = FileField('upload logo', validators = [FileAllowed(['jpg', 'png', 'jpeg'])])
    web = StringField('Web url', validators = [DataRequired(), Length(min=2)])
    deadline = StringField('Deadline', validators = [DataRequired(), Length(min=2)])     
    submit = SubmitField('Submit')