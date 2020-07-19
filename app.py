from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = '0b14be815347c845022cdeeb6c5937f6'
posts = [
    {
      'author' : 'SANA',
      'title' : 'Faso',
      'content' : 'Electronic',
      'date_posted' : '01/10/2020'  
    },
    {
      'author' : 'Aloute',
      'title' : 'Burkina ',
      'content' : 'Electronic',
      'date_posted' : '01/03/2020'   
    },
    {
      'author' : 'SANA Aloute',
      'title' : 'Burkina Faso',
      'content' : 'Electronic',
      'date_posted': '01/01/2020'   
    }

]



@app.route('/',methods=['POST', 'GET'])
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',posts=posts)

@app.route('/register',methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/login/',methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'password' :
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Unsuccessful log in. Please check username and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)


if __name__ == '__main__':
    app.run(debug=True)    
