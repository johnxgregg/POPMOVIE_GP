from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.user import User
# from flask_app.models.    import
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('landing_page.html')

@app.route('/sign_in')
def landing_sign_in():
    return render_template('login.html')


@app.route('/register')
def landing_register():
    return render_template('register.html')


@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/register')
    data ={ 
        "username": request.form['username'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')


@app.route('/sign_in',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Enter Email and Password","login")
        return redirect('/sign_in')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Enter Password","login")
        return redirect('/sign_in')
    session['user_id'] = user.id
    return redirect('/dashboard')


# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data ={
#         'id': session['user_id']
#     }
#     return render_template("dashboard.html",user=User.get_by_id(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
