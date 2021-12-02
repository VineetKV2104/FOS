from flask import Flask, request,render_template, redirect, session
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, request, session
from flask_session import Session



app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fos.db' 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQLAlchemy(app)

class Superlogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    
@app.route('/login', methods=["GET","POST"])
def Login():
    if request.method=="POST":
        if request.form['uname'] == '' or request.form['pass'] == '':
            return redirect("/login")
        creds = Superlogin.query.filter_by(username = request.form['uname'], password = request.form['pass']).first()
        print(creds)
        if creds == None:
            return redirect("/login")
        else:
            session["name"] = request.form['uname']
            return redirect("/admin")

    return render_template("admin/login.html")

@app.route('/logout', methods=["GET","POST"])
def logout():
    session.clear()
    return redirect('/login')

@app.route('/admin', methods=["GET","POST"])
def admin():
    if not session.get("name"):
            return redirect("/login")

    return render_template("admin/index.html")
if __name__ == '__main__':
   app.run(debug=True)


