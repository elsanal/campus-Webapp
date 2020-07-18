from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = '0b14be815347c845022cdeeb6c5937f6'
posts = [
    {
      'author' : 'SANA',
      'country' : 'Faso',
      'major' : 'Electronic'   
    },
    {
      'author' : 'Aloute',
      'country' : 'Burkina ',
      'major' : 'Electronic'   
    },
    {
      'author' : 'SANA Aloute',
      'country' : 'Burkina Faso',
      'major' : 'Electronic'   
    }

]



@app.route('/',methods=['POST', 'GET'])
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',posts=posts)

@app.route('/register')
def register():
    form = RegistrationForm()
    print(app.url_map)
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'sucess')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/login/')
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Login', form = form)


if __name__ == '__main__':
    app.run(debug=True)    
