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

class Tax(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tax_type = db.Column(db.String)
    tax_value = db.Column(db.String)

class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuisine_name = db.Column(db.String)

class FoodFilters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filter_name = db.Column(db.String)

class IngCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ing_cat_name = db.Column(db.String)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ing_name = db.Column(db.String)
class RestActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String)

class HomeSetting(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    logo=db.Column(db.String)
    rest_name=db.Column(db.String)
    rest_location=db.Column(db.String)
    table_no=db.Column(db.String)
    rest_address=db.Column(db.String)
    rest_contact_no=db.Column(db.Integer)
    gst_no=db.Column(db.String)

class FeatureSlides(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    feature_name=db.Column(db.String)
    feature_img=db.Column(db.String)

class MenuCategory(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    food_category_name=db.Column(db.String)
    
class FoodMenuItem(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    food_item_name=db.Column(db.String)
    food_item_rate=db.Column(db.Integer)
    ingredients=db.Column(db.String)
    food_item_img=db.Column(db.String)

class OrderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String)
    person_name = db.Column(db.String)
    sgst = db.Column(db.Float)
    cgst = db.Column(db.Float)
    bill_amount = db.Column(db.Float)
    offer = db.Column(db.String)

class OrderItems(db.Model):
    order_detail_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String)
    person_name = db.Column(db.String)
    rate = db.Column(db.Float)
    cooking_instructions = db.Column(db.String)
    general_instructions = db.Column(db.String)


@app.route('/login', methods=["GET","POST"])
def Login():
    if request.method=="POST":
        if request.form['uname'] == '' or request.form['pass'] == '':
            return redirect("/login")
        creds = Superlogin.query.filter_by(username = request.form['uname'], password = request.form['pass']).first()
        
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

@app.route('/')
def index():
    return render_template('')


@app.route('/orders')
def order():
    return render_template('front_end/orders.html')


@app.route('/checkout')
def checkout():
    return render_template('front_end/checkout.html')


@app.route('/cart')
def cart():
    return render_template('front_end/cart.html')


if __name__ == '__main__':
   app.run(debug=True)


