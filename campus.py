from flask import Flask, render_template, url_for, request,redirect, flash
from forms import RegisterForm, LoginForm, JobForm, UniversityForm, ScholarshipForm, CalendarForm
import os, secrets
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import firebase_admin
from firebase import storage, Firebase 
from firebase_admin import credentials
from firebase_admin import firestore, storage
from werkzeug.utils import secure_filename
from random import random
import json



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
    # random_index = random.radint(2,5)
    dataScho = firestore.collection(u'Scholarship').get()
    docsScho = []
    for doc in dataScho:
        docsScho.append(doc.to_dict())
        
    dataUni = firestore.collection(u'Universities').get()
    docsUni = []
    for doc in dataUni:
        docsUni.append(doc.to_dict())
        
    dataJobStage = firestore.collection(u'JobsStages').get()
    docsJobStage = []
    for doc in dataJobStage:
        docsJobStage.append(doc.to_dict())        
    return render_template('index.html', docsJobStage = docsJobStage, 
                           docsScho = docsScho, docsUni = docsUni)

@app.route("/index/about")
def about():
    form = CalendarForm
    return render_template('index/about.html', title = "About", form = form)

################### authentification

@app.route("/auth/login",methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html', title = "login")


@app.route("/auth/register",methods=['GET', 'POST'])
def register():
    return render_template('auth/register.html')

################ Scholarship
@app.route("/pages/scholarship",methods=['GET', 'POST'])
def scholarship():
    data = firestore.collection(u'Scholarship').get()
    docs = []
    for doc in data:
        docs.append(doc.to_dict())
    return render_template('pages/scholarship.html', title = "scholarship", docs = docs)



#University
@app.route("/pages/university",methods=['GET', 'POST'])
def university():
    data = firestore.collection(u'Universities').get()
    docs = []
    for doc in data:
        docs.append(doc.to_dict())
    return render_template('pages/university.html', title = "university", docs = docs)


################## Details

@app.route('/details/scholarship_details/<int:index>',methods=['GET'])
def scholarship_details(index):
    data = firestore.collection(u'Scholarship').get()
    docs = []
    for doc in data:
        docs.append(doc.to_dict())
    return render_template('details/scholarship_details.html', document = docs[index])

@app.route('/details/university_details/<int:index>',methods=['GET'])
def university_details(index):
    data = firestore.collection(u'Universities').get()
    docs = []
    for doc in data:
        docs.append(doc.to_dict())
    return render_template('details/university_details.html', document = docs[index])

@app.route('/details/job_details/<int:index>',methods=['GET'])
def job_details(index):
    data = firestore.collection(u'jobStages').get()
    docs = []
    for doc in data:
        docs.append(doc.to_dict())
    return render_template('details/job_details.html', document = docs[index])


# make a post
@app.route("/pages/nouveaux",methods=['GET', 'POST'])
def nouveaux():
    data = firestore.collection(u'Scholarship').get()
    docs = []
    for doc in data:
        docs.append(doc.to_dict())
    return render_template('pages/nouveaux.html', title = "nouveaux", docs = docs)

@app.route("/pages/jobs&stages",methods=['GET', 'POST'])
def jobStage():
    data = firestore.collection(u'Scholarship').get()
    docs = []
    for doc in data:
        docs.append(doc.to_dict())
    return render_template('pages/jobs&stages.html', title = "jobs&stages", docs = docs)

@app.route("/pages/contacts",methods=['GET', 'POST'])
def contact():
    return render_template('pages/contacts.html', title = "contacts")



           ########  Admin upload to database ################  

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
@app.route("/admin/makeJob",methods=['GET', 'POST'])
def makeJob():
    form = JobForm()
    if form.validate_on_submit():
        print('this is a new uni')
        flash(f'sucessfully created', 'success')
        if form.logo.data:
            print('file picked')
            picture = save_logo(form.logo.data)
            picture_path = os.path.join(app.root_path,'photos',picture)
            saveUni_toDatabase(form, picture, picture_path)
            os.remove(picture_path)
            return redirect(url_for('home'))
    return render_template('admin/makeJob.html', form = form)


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
  
  
  ################## Save Job to DB  
def saveJob_toDatabase(form, logo, picture_path):
    firebase.storage().child('JobStage').child(logo).put(picture_path)
    logoUrl = firebase.storage().child('JobStage').child(logo).get_url(None)
    docRef = firestore.collection(u'JobStage')
    docRef.add({
    u'name' : u'{}'.format(request.form.get('name')),
    u'description' : u'{}'.format(request.form.get('description')),
    u'position' : u'{}'.format(request.form.get('position')),
    u'country' : u'{}'.format(request.form.get('country')),
    u'deadline' : form.deadline.data.strftime('%d/%m/%Y'),
    u'level' : u'{}'.format(request.form.get('level')),
    u'logo' : logoUrl,
    u'webUrl' : u'{}'.format(request.form.get('web')),
    u'order': u'{}'.format(form.post_order),
    })     
    
    
    
      

if __name__ == "__main__":
    app.run(debug=True)

   