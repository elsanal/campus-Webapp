from flask import Flask, render_template, url_for, request,redirect, flash
from forms import RegisterForm, LoginForm, PostForm, UniversityForm, ScholarshipForm
import os, secrets
from PIL import Image
import firebase_admin
from firebase import storage, Firebase 
from firebase_admin import credentials
from firebase_admin import firestore, storage
from werkzeug.utils import secure_filename
# import flask_resize


app = Flask(__name__)
app.config['SECRET_KEY'] = '20fe18bd517a11a1e26759b5664882b0'
firebaseConfig = {
            'apiKey': "AIzaSyCb3LNJ55ctSuAvmxQNHArY77bRtjlBdnw",
            'authDomain': "campus-494ee.firebaseapp.com",
            'databaseURL': "https://campus-494ee.firebaseio.com",
            'projectId': "campus-494ee",
            'storageBucket': "campus-494ee.appspot.com",
            'messagingSenderId': "935121093075",
            'appId': "1:935121093075:web:ee337dcb8c5769bacaaf26",
            'measurementId': "G-WRNFW5KML9"
        }

cred = credentials.Certificate("/Users/sanaaloute/firebase-sdk.json")
firebase_admin.initialize_app(cred)
firestore = firestore.client()
firebase = Firebase(firebaseConfig)
database = firebase.database()



# index

@app.route("/",methods=['GET', 'POST'])
@app.route("/index")
def home():
    image = url_for('static', filename='img/background-image.jpg')
    return render_template('index.html', posts = image)

@app.route("/index/about")
def about():
    return render_template('index/about.html', title = "About")

# authentification

@app.route("/auth/login",methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html', title = "login")


@app.route("/auth/register",methods=['GET', 'POST'])
def register():
    return render_template('auth/register.html')

# Scholarship

@app.route("/scholarship/scholarship",methods=['GET', 'POST'])
def scholarship():
    return render_template('scholarship/scholarship.html', title = "scholarship")



#University

@app.route("/university/university",methods=['GET', 'POST'])
def university():
    return render_template('university/university.html', title = "university")



# make a post

@app.route("/post/videos",methods=['GET', 'POST'])
def videos():
    return render_template('post/videos.html', title = "videos")

########  Admin upload to database

@app.route("/admin/makeScho",methods=['GET', 'POST'])
def makeScho():
    form = ScholarshipForm()
    return render_template('admin/makeScho.html', form = form)

@app.route("/admin/makeUni",methods=['GET', 'POST'])
def makeUni():
    form = UniversityForm()
    return render_template('admin/makeUni.html',form = form)

@app.route("/admin/makepost",methods=['GET', 'POST'])
def makepost():
    form = PostForm()
    if form.validate_on_submit():
        flash(f'sucessfully created', 'success')
        if form.picture.data:
            # file = form.picture.data
            print('file pciked')
            picture = save_picture(form.picture.data)
            picture_path = os.path.join(app.root_path,'photos',picture)
            firebase.storage().child('Jesuis').child(picture).put(picture_path)
            url = firebase.storage().child('Jesuis').child(picture).get_url(None)
            os.remove(picture_path)
            ecole_ref = firestore.collection(u'Ecole')
            ecole_ref.document(u'time').set({
            u'name' : u'{}'.format(request.form.get('title')),
            u'description' : u'{}'.format(request.form.get('description')),
            u'image' : url,
            u'date'  : u'{}'.format(form.post_date),
            u'time' : u'{}'.format(form.post_time)
            })
        print(form.post_date)
        return redirect(url_for('home'))
    return render_template('admin/makepost.html', form = form)

def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _,file_ext = os.path.splitext(form_pic.filename)
    picture_name = random_hex + file_ext
    picture_path = os.path.join(app.root_path,'photos',picture_name)
    form_pic.save(picture_path)
    out_size = (150,150)
    image = Image.open(form_pic)
    image.thumbnail(out_size)
    image.save(picture_path)
    return picture_name

if __name__ == "__main__":
    app.run(debug=True)

   