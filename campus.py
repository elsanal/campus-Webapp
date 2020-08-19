from flask import Flask, render_template, url_for, request,redirect, flash
from forms import RegisterForm, LoginForm, PostForm, UniversityForm, ScholarshipForm
import os, secrets
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import firebase_admin
from firebase import storage, Firebase 
from firebase_admin import credentials
from firebase_admin import firestore, storage
from werkzeug.utils import secure_filename



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



######################## index

@app.route("/",methods=['GET', 'POST'])
@app.route("/index")
def home():
    data = firestore.collection(u'Photos_videos').get()
    docs = []
    for doc in data:
        docs.append(doc.to_dict())
    return render_template('index.html', docs = docs)

@app.route("/index/about")
def about():
    return render_template('index/about.html', title = "About")

################### authentification

@app.route("/auth/login",methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html', title = "login")


@app.route("/auth/register",methods=['GET', 'POST'])
def register():
    return render_template('auth/register.html')

################ Scholarship
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

########### upload new scholarship
@app.route("/admin/makeScho",methods=['GET', 'POST'])
def makeScho():
    form = ScholarshipForm()
    if form.validate_on_submit():
        flash(f'sucessfully created', 'success')
        if form.logo.data:
            print('file pciked')
            picture = save_logo(form.logo.data)
            picture_path = os.path.join(app.root_path,'photos',picture)
            saveScho_toDatabase(form, picture, picture_path)
            os.remove(picture_path)
            return redirect(url_for('home'))
    return render_template('admin/makeScho.html', form = form)

########## upload new University
@app.route("/admin/makeUni",methods=['GET', 'POST'])
def makeUni():
    
    form = UniversityForm()
    if form.validate_on_submit():
        print('this is a new uni')
        flash(f'sucessfully created', 'success')
        if form.logo.data:
            print('file pciked')
            picture = save_logo(form.logo.data)
            picture_path = os.path.join(app.root_path,'photos',picture)
            saveUni_toDatabase(form, picture, picture_path)
            os.remove(picture_path)
            return redirect(url_for('home'))
    return render_template('admin/makeUni.html',form = form)


######### Make a new post
@app.route("/admin/makepost",methods=['GET', 'POST'])
def makepost():
    form = PostForm()
    if form.validate_on_submit():
        flash(f'sucessfully created', 'success')
        if form.picture.data:
            print('file pciked')
            picture = save_picture(form.picture.data)
            picture_path = os.path.join(app.root_path,'photos',picture)
            savePost_toDatabase(form, picture, picture_path)
            os.remove(picture_path)
            return redirect(url_for('home'))
    return render_template('admin/makepost.html', form = form)

####### Resize and save picture
def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _,file_ext = os.path.splitext(form_pic.filename)
    picture_name = random_hex + file_ext
    picture_path = os.path.join(app.root_path,'photos',picture_name)
    form_pic.save(picture_path)
    out_size = (1000,800)
    image = Image.open(form_pic)
    image.thumbnail(out_size)
    image.save(picture_path)
    return picture_name

####### Resize and save picture
def save_logo(form_pic):
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

################# Save a post
def savePost_toDatabase(form, picture, picture_path):
    firebase.storage().child('PostImages').child(picture).put(picture_path)
    ImageUrl = firebase.storage().child('PostImages').child(picture).get_url(None)
    docRef = firestore.collection(u'Photos_videos')
    docRef.add({
    u'title' : u'{}'.format(request.form.get('title')),
    u'description' : u'{}'.format(request.form.get('description')),
    u'image' : ImageUrl,
    u'date'  : u'{}'.format(form.post_date),
    u'time' : u'{}'.format(form.post_time),
    u'order': u'{}'.format(form.post_order),
    u'owner': u'eT1yo6RHBZNEz3smyKyzwZ0fQFV2',
    u'type' : u'photo',
    u'webUrl': u'webUrl',
    })

########### Save an university

def saveUni_toDatabase(form, logo, picture_path):
    firebase.storage().child('Universities').child(logo).put(picture_path)
    logoUrl = firebase.storage().child('Universities').child(logo).get_url(None)
    docRef = firestore.collection(u'Universities')
    docRef.add({
    u'name' : u'{}'.format(request.form.get('name')),
    u'description' : u'{}'.format(request.form.get('description')),
    u'majors' : u'{}'.format(request.form.get('major')),
    u'country' : u'{}'.format(request.form.get('country')),
    u'deadline' : form.deadline.data.strftime('%d/%m/%Y'),
    u'level' : u'{}'.format(request.form.get('level')),
    u'logo' : logoUrl,
    u'webUrl' : u'{}'.format(request.form.get('web')),
    u'date'  : u'{}'.format(form.post_date),
    u'order': u'{}'.format(form.post_order),
    })

#############save a scholarship

def saveScho_toDatabase(form, logo, picture_path):
    firebase.storage().child('Scholarship').child(logo).put(picture_path)
    logoUrl = firebase.storage().child('Scholarship').child(logo).get_url(None)
    docRef = firestore.collection(u'Scholarship')
    docRef.add({
    u'name' : u'{}'.format(request.form.get('name')),
    u'description' : u'{}'.format(request.form.get('description')),
    u'advantage' : u'{}'.format(request.form.get('advantage')),
    u'country' : u'{}'.format(request.form.get('country')),
    u'deadline' : form.deadline.data.strftime('%d/%m/%Y'),
    u'level' : u'{}'.format(request.form.get('level')),
    u'logo' : logoUrl,
    u'webUrl' : u'{}'.format(request.form.get('web')),
    u'date'  : u'{}'.format(form.post_date),
    u'order': u'{}'.format(form.post_order),
    
    })    

if __name__ == "__main__":
    app.run(debug=True)

   