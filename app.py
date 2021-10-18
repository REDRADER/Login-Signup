
from enum import unique
from os import name
from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect



app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/users'

app.secret_key = 'thisistest'

db=SQLAlchemy(app)




class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False,unique=True)
    password=db.Column(db.String(200),nullable=False,unique=True)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name


      
    

@app.route("/register", methods=['POST','GET'])
def register():

    msg=''
    if request.method=='POST':
        name=request.form['name']
        femail=request.form['email']
        password=request.form['pass']
        
        user=Users.query.filter_by(email=femail).first()

        if user is None:
            new_u=Users(name=name,email=femail,password=password)
            try:
                db.session.add(new_u)
                db.session.commit()
                msg="Account created succefully"
                return redirect('/login')
            except:
                return"there was a error adding data"
        else:
            msg="Account already exists"
    return render_template("register.html",msg=msg)
    

@app.route("/login",methods=['POST','GET'])
def login():
    msg=''
    if request.method=='POST' and 'email' in request.form and 'pass' in request.form:
        email=request.form['email']
        password=request.form['pass']
        user=Users.query.filter_by(email=email,password=password).first()
        if user:
            session['loggedin'] = True
            session['id'] = user.id
            session['name'] = user.name
            return redirect('/')
        else:
            msg="wrong email passwod"

    return render_template("login.html",msg=msg)
        
            
@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('name',None)
    return redirect("/login")
    
    

@app.route("/")
def index():
    if 'loggedin' in session:
        user=Users.query.filter_by(id=session['id']).first()
        return render_template("index.html",user=user)
    return redirect("/login")
    




if __name__ =="__main__":
    app.run(debug=True)