'''
from flask import render_template, url_for, session, flash
from attendance import app
from flask import request
from flask import redirect
from attendance.flask_wtf import FlaskForm
from attendance.wtforms import StringField
from attendance.wtforms import Form, SelectField, SubmitField, TextAreaField, TextField, validators, ValidationError
from attendance.wtforms.validators import DataRequired, Length
# flask login 
from attendance.flask_login import LoginManager
from attendance.flask_login import UserMixin
from attendance.functools import wraps
'''
from flask import render_template, url_for, session, flash
from attendance import app
from flask import request
from flask import redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import Form, SelectField, SubmitField, TextAreaField, TextField, validators, ValidationError
from wtforms.validators import DataRequired, Length
# flask login 
from flask_login import LoginManager
from flask_login import UserMixin
from functools import wraps

# database 
from attendance.modules import *

from attendance.forms import *
'''
# create form for flask (user view page )
class new_user(FlaskForm):
    fname = StringField("first name",[validators.length(min=1, max=40), validators.input_required()])
    lname = StringField("last name ",[validators.length(min=1, max=40), validators.input_required()])
    student_id = StringField("student id",[validators.length(min=4, max=10), validators.input_required()])
    auth = StringField("authorisation",[validators.length(min=4, max=20), validators.input_required()])

# create user table in database 
class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=True)
    lname = db.Column(db.String(20), nullable=True)
    student_id = db.Column(db.Integer)
    auth = db.Column(db.String(20))

db.create_all()


def __repr__(self):
        return "<first name: {}>".format(self.fname)
'''
# login required decorator 
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else: 
            flash('you need to login first')
            return redirect(url_for('login'))
    return wrap

#route for home page
@app.route('/', methods=["GET", "POST"])
@login_required
def home():
   
    return render_template('home.html')

# create route for welcome page 
@app.route('/welcome') 
def welcome():
    return render_template("welcome.html")


# route for login page  
@app.route('/login', methods=["POST", "GET"])
def login():
    error = None 
    if request.method == "POST":
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'incorrect credentials ' # error message change later 
        else:  
            # session 
            session['logged_in'] = True 
            flash("you're logged in ")
            return redirect(url_for('home'))
    return render_template("login.html", error=error)

# create logout page 
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash("you're now logged out")
    return redirect(url_for('welcome'))


# route to add and view different users 
@app.route('/view_user', methods=["GET", "POST"])
def view_user():
    form = new_user()
    if request.form:
        user = User(fname=form.fname.data, lname=form.lname.data, student_id=form.student_id.data, auth=form.auth.data)
        db.session.add(user)
        db.session.commit()
    users = User.query.all()
    return render_template('view_user.html', users=users, form=form)

# update route to update fname in user 
@app.route("/update", methods=["POST"])
def update():
    newfname = request.form.get("newfname")
    oldfname = request.form.get("oldfname")
    newlname = request.form.get("newlname")
    oldlname = request.form.get("oldlname")
    newstudent_id = request.form.get("newstudent_id")
    oldstudent_id = request.form.get("oldstudent_id")
    newauth = request.form.get("newauth")
    oldauth = request.form.get("oldauth")
    user = User.query.filter_by(fname=oldfname, lname=oldlname).first()
    if newfname != None:
        user.fname = newfname
    if newlname != None:
        user.lname = newlname
    if newstudent_id != None:
        user.student_id = newstudent_id
    if newauth != None:
        user.auth = newauth
    db.session.commit()
    return redirect('/view_user')

# delete route to delete fname in user
@app.route("/delete", methods=["POST"])
def delete():
    fname = request.form.get("fname")
    user = User.query.filter_by(fname=fname).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/view_user")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404