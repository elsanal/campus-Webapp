from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, 
                     BooleanField, TextAreaField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import date, datetime
import calendar
import tempfile, os
import firebase

today = date.today()
date = today.strftime("%d/%m/%Y")

now = datetime.now()
time = now.strftime('%H : %M')
order = now.strftime('%y:%m:%d:%H:%M:%S')

###### Registration form

class RegisterForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired(), Email(),])
    password = PasswordField('Password', validators = [DataRequired(),])
    confirm_password = PasswordField('Confirm password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign In')
###### Login form

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email(),])
    password = PasswordField('Password', validators = [DataRequired(),])
    submit = SubmitField('Log In')
       

########## Upload a Job
class JobForm(FlaskForm):
    company_name = StringField('Company name', validators = [DataRequired(), Length(min=2)])
    description = TextAreaField('Description', validators = [DataRequired(), Length(min=2)])
    country = StringField('Country', validators = [DataRequired(), Length(min=2),])
    logo = FileField("Upload logo", validators=[FileAllowed(['jpg', 'png', 'mp4','jpeg'])])
    web = StringField('Website url', validators = [DataRequired(), Length(min=2),])
    condition = TextAreaField('Conditions', validators = [DataRequired(),])
    position = TextAreaField('Positions', validators = [DataRequired(),])
    how_to_apply = TextAreaField('How to apply', validators = [DataRequired(),])
    deadline = DateField('Deadline')
    submit = SubmitField('Submit')
    post_order = order
  
    
    

##########   Upload university  
class UniversityForm(FlaskForm):
    university_name = StringField('University name', validators = [DataRequired(), Length(min=2,)])
    country = StringField('Country', validators = [DataRequired(), Length(min=2),])
    description = TextAreaField('Description', validators = [DataRequired(),])
    major = TextAreaField('Majors', validators = [DataRequired(), ])
    logo = FileField("Upload logo", validators=[FileAllowed(['jpg', 'png', 'mp4','jpeg'])])
    web = StringField('Website url', validators = [DataRequired(), Length(min=2),])
    top = TextAreaField('is it top?', validators = [DataRequired(),])
    deadline = DateField('Deadline')
    post_date = date
    post_order = order    
    submit = SubmitField('Submit')

##########  Upload Scholarship     
class ScholarshipForm(FlaskForm):
    scholarship_name = StringField('Scholarship name', validators = [DataRequired(), Length(min=2,)])
    country = StringField('Country', validators = [DataRequired(), Length(min=2),])
    description = TextAreaField('Description', validators = [DataRequired(),])
    condition = TextAreaField('Conditions', validators = [DataRequired(),])
    advantage = TextAreaField('Advantages', validators = [DataRequired(),])
    level = StringField('level', validators = [DataRequired(),])
    logo = FileField('upload logo', validators = [FileAllowed(['jpg', 'png', 'jpeg',])])
    web = StringField('Website url', validators = [DataRequired(), Length(min=2)])
    how_to_apply = TextAreaField('How to apply', validators = [DataRequired(),])
    popular = TextAreaField('is it popular?', validators = [DataRequired(),])
    deadline = DateField('Deadline',) 
    post_date = date
    post_order = order   
    submit = SubmitField('Submit')
    
class CalendarForm(FlaskForm):
    calendar = calendar.calendar(2017)    