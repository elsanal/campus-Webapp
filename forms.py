from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, 
                     BooleanField, TextAreaField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import date, datetime
import tempfile, os
import firebase

today = date.today()
date = today.strftime("%d/%m/%Y")

now = datetime.now()
time = now.strftime("%H : %M")

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
    name = StringField('University name', validators = [DataRequired(), Length(min=2,)])
    country = StringField('Country', validators = [DataRequired(), Length(min=2),])
    description = TextAreaField('Description', validators = [DataRequired(),])
    major = TextAreaField('Majors', validators = [DataRequired(), ])
    logo = FileField("Upload logo", validators=[FileAllowed(['jpg', 'png', 'mp4','jpeg'])])
    web = StringField('Website url', validators = [DataRequired(), Length(min=2),])
    deadline = DateField('Deadline', format='%Y-%m-%d')
    post_date = date
    post_time = time    
    submit = SubmitField('Submit')

##########  Upload Scholarship     
class ScholarshipForm(FlaskForm):
    name = StringField('Scholarship name', validators = [DataRequired(), Length(min=2,)])
    country = StringField('Country', validators = [DataRequired(), Length(min=2),])
    description = TextAreaField('Description', validators = [DataRequired(),])
    advantage = TextAreaField('Advantages', validators = [DataRequired(),])
    level = StringField('level', validators = [DataRequired(),])
    logo = FileField('upload logo', validators = [FileAllowed(['jpg', 'png', 'jpeg',])])
    web = StringField('Website url', validators = [DataRequired(), Length(min=2)])
    deadline = DateField('Deadline', format='%Y-%m-%d') 
    post_date = date
    post_time = time   
    submit = SubmitField('Submit')