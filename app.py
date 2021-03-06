from flask import render_template, jsonify
from flask_sqlalchemy import model
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
import settings
from settings import app, db
import models


api = Api(app)


# ------------------------- Super Admin Authentication Section Starts -------------------- 
@app.route('/login', methods=["GET","POST"])
def Login():
    if settings.request.method=="POST":
        if settings.request.form['uname'] == '' or settings.request.form['pass'] == '':
            return settings.redirect("/login")
        creds = models.Superlogin.query.filter_by(username = settings.request.form['uname'], password = settings.request.form['pass']).first()
        
        if creds == None:
            return settings.redirect("/login")
        else:
            settings.session["name"] = settings.request.form['uname']
            return settings.redirect("/admin")

    return settings.render_template("admin/login.html")

@app.route('/logout', methods=["GET","POST"])
def logout():
    settings.session.clear()
    return settings.redirect('/login')

@app.route('/admin', methods=["GET","POST"])
def admin():
    if not settings.session.get("name"):
        return settings.redirect("/login")
        
    return settings.render_template("admin/index.html")


# ------------------------- Super Admin Authentication Section Ends -------------------- 

# ------------------------- Food Menu Category Section Starts -------------------- 
@app.route('/foodcat', methods=["GET","POST"]) # End Point to Add & View the Menu Categories
def foodcat():
    if not settings.session.get("name"):
            return settings.redirect("/login")
    if settings.request.method=="POST":
        food_category_name = settings.request.form["food_category_name"]
        info=models.MenuCategory(food_category_name=food_category_name)
        db.session.add(info)
        db.session.commit()
    fetch=models.MenuCategory.query.all() 
    return settings.render_template('admin/foodcat.html', getinfo=fetch)

@app.route('/foodcatupdater', methods=["GET","POST"]) # End Point to Update Menu Category
def foodcatupdater():
    if not settings.session.get("name"):
            return settings.redirect("/login")
    if settings.request.method=="POST":
        id = settings.request.form['id']
        food_category_name = settings.request.form["food_category_name"]
        fetch=models.MenuCategory.query.filter_by(id=id).first()
        fetch.food_category_name=food_category_name
        db.session.commit()
        return settings.redirect("/foodcat")

@app.route('/foodcatupdate', methods=["GET","POST"]) # End Point to Update Menu Category Continued
def foodcatupdate():
    if not settings.session.get("name"):
            return settings.redirect("/login")
    id = settings.request.args['id']
    fetch=models.MenuCategory.query.filter_by(id=id).all()
    return settings.render_template("admin/update_foodcat.html",getinfo=fetch)

@app.route('/foodcatdel/<int:id>', methods=["GET","POST"]) # End Point to Add the Menu Categories
def foodcatdel(id):
    if not settings.session.get("name"):
            return settings.redirect("/login")
    fetch=models.MenuCategory.query.filter_by(id=id).first()
    db.session.delete(fetch)
    db.session.commit()
    return settings.redirect("/foodcat")

# ------------------------- Food Menu Category Section Ends -----------------------




# ------------------------- Fooditems Section Starts -------------------- 
@app.route('/fooditem', methods=["GET","POST"]) # End Point to Add & View the Filters
def fooditems():
    if not settings.session.get("name"):
        return settings.redirect("/login")
    if settings.request.method=="POST":
        fooditemname=settings.request.form["fooditemname"]
        fooditemrate=settings.request.form["fooditemrate"]
        fooditemimg=settings.request.files["fooditemimg"]
        fooditemcat=settings.request.form["fooditemcat"]
        fooditemfilter=settings.request.form["fooditemfilter"]
        fooditemcuisine=settings.request.form["fooditemcuisine"]
        ing_name = settings.request.form.getlist("ing_name") 
        fooditemimg.seek(0, settings.os.SEEK_END)
        if fooditemimg.tell()==0:
            pass
        fooditemimg.seek(0)
        fname='static/images/fooditem/'+secure_filename(fooditemimg.filename)
        fooditemimg.save(fname)
        addfooditem=models.FoodMenuItem(food_item_name=fooditemname, food_item_rate=fooditemrate, food_item_cat=fooditemcat, food_item_filter=fooditemfilter, food_item_cuisine=fooditemcuisine, ingredients=ing_name)
        db.session.add(addfooditem)
        db.session.commit()

    ingredientdata=models.MenuCategory.query.all()
    fooditemdata=models.FoodMenuItem.query.all()
    filterfetch=models.FoodFilters.query.all()
    cuisinefetch=models.Cuisine.query.all()
    return settings.render_template('admin/fooditem.html', ingredientdata=ingredientdata, fooditemdata=fooditemdata, filterfetch=filterfetch, cuisinefetch=cuisinefetch)

@app.route('/fooditemupdate', methods=["GET","POST"]) # End Point to Update Food Menu Item Continued
def foodmenuitemupdate():
    if not settings.session.get("name"):
        return settings.redirect("/login")
    if settings.request.method=="POST":
        id = settings.request.form['id']
        fooditemname=settings.request.form["fooditemname"]
        fooditemrate=settings.request.form["fooditemrate"]
        fooditemcat=settings.request.form["fooditemcat"]
        fooditemfilter=settings.request.form["fooditemfilter"]
        fooditemcuisine=settings.request.form["fooditemcuisine"]
        ing_name = settings.request.form["ing_name"] 
        fooditemdata=models.FoodMenuItem.query.filter_by(id=id).all()
        fooditemdata.food_item_name=fooditemname
        fooditemdata.food_item_rate=fooditemrate
        fooditemdata.food_item_cat=fooditemcat
        fooditemdata.food_item_filter=fooditemfilter
        fooditemdata.food_item_cuisine=fooditemcuisine
        fooditemdata.ing_name=ing_name
        db.session.commit()
        return settings.redirect("/fooditem")

    id = settings.request.args['id']
    fooditemdata=models.FoodMenuItem.query.filter_by(id=id).all()
    fetching=models.Ingredient.query.all()
    ingredientdata=models.MenuCategory.query.all()
    filterfetch=models.FoodFilters.query.all()
    cuisinefetch=models.Cuisine.query.all()
    return settings.render_template("admin/update_fooditem.html", fooditemdata=fooditemdata, ingredientdata=ingredientdata, filterfetch=filterfetch, cuisinefetch=cuisinefetch, fetching = fetching)

@app.route('/foodmenuitemdel/<int:id>', methods=["GET","POST"]) # End Point to Delete Ingredient
def foodmenuitemdel(id):
    if not settings.session.get("name"):
        return settings.redirect("/login")
    fetch=models.FoodMenuItem.query.filter_by(id=id).first()
    db.session.delete(fetch)
    db.session.commit()

    fetch_ing=models.FoodIngredients.query.filter_by(fid=id).all()
    for f in fetch_ing:
        db.session.delete(f)
        db.session.commit()
    return settings.redirect("/fooditem")
# ------------------------- Fooditems Section Ends -------------------- 

# -------------------------  Filters Section Starts -------------------- 

@app.route('/filters', methods=["GET","POST"]) # End Point to Add & View the Filters
def filters():
    if not settings.session.get("name"):
            return settings.redirect("/login")
    if settings.request.method=="POST":
        filter_name = settings.request.form["filter_name"]
        info=models.FoodFilters(filter_name=filter_name)
        db.session.add(info)
        db.session.commit()
    fetch=models.FoodFilters.query.all() 
    return settings.render_template('admin/filters.html', getinfo=fetch)

@app.route('/filtersupdater', methods=["GET","POST"]) # End Point to Update Filters
def filtersupdater():
    if not settings.session.get("name"):
            return settings.redirect("/login")
    if settings.request.method=="POST":
        id = settings.request.form['id']
        filter_name = settings.request.form["filter_name"]
        fetch=models.FoodFilters.query.filter_by(id=id).first()
        fetch.filter_name=filter_name
        db.session.commit()
        return settings.redirect("/filters")

@app.route('/filtersupdate', methods=["GET","POST"]) # End Point to Update Filters Continued
def filtersupdate():
    if not settings.session.get("name"):
            return settings.redirect("/login")
    id = settings.request.args['id']
    fetch=models.FoodFilters.query.filter_by(id=id).all()
    return settings.render_template("admin/update_filters.html",getinfo=fetch)

@app.route('/filtersdel/<int:id>', methods=["GET","POST"]) # End Point to Del the Filters
def filtersdel(id):
    if not settings.session.get("name"):
            return settings.redirect("/login")
    fetch=models.FoodFilters.query.filter_by(id=id).first()
    db.session.delete(fetch)
    db.session.commit()
    return settings.redirect("/filters")

# ------------------------- Filters Section Ends -------------------- 

# -------------------------  Tax Section Starts -------------------- 

@app.route('/tax', methods=["GET","POST"]) # End Point to Add & View the Tax
def tax():
    if not settings.session.get("name"):
            return settings.redirect("/login")
    if settings.request.method=="POST":
        tax_type = settings.request.form["tax_type"]
        tax_value = settings.request.form["tax_value"]
        info=models.Tax(tax_type=tax_type,tax_value=tax_value)
        db.session.add(info)
        db.session.commit()
    fetch=models.Tax.query.all() 
    return settings.render_template('admin/tax.html', getinfo=fetch)

@app.route('/taxupdater', methods=["GET","POST"]) # End Point to Update Tax
def taxupdater():
    if not settings.session.get("name"):
            return settings.redirect("/login")
    if settings.request.method=="POST":
        id = settings.request.form['id']
        tax_type = settings.request.form["tax_type"]
        tax_value = settings.request.form["tax_value"]
        fetch=models.Tax.query.filter_by(id=id).first()
        fetch.tax_type=tax_type
        fetch.tax_value=tax_value
        db.session.commit()
        return settings.redirect("/tax")

@app.route('/taxupdate', methods=["GET","POST"]) # End Point to Update Tax Continued
def taxupdate():
    if not settings.session.get("name"):
            return settings.redirect("/login")
    id = settings.request.args['id']
    fetch=models.Tax.query.filter_by(id=id).all()
    return settings.render_template("admin/update_tax.html",getinfo=fetch)

@app.route('/taxdel/<int:id>', methods=["GET","POST"]) # End Point to Del the Tax
def taxdel(id):
    if not settings.session.get("name"):
            return settings.redirect("/login")
    fetch=models.Tax.query.filter_by(id=id).first()
    db.session.delete(fetch)
    db.session.commit()
    return settings.redirect("/tax")

# ------------------------- Tax Section Ends -------------------- 

# -------------------------  Cuisine Section Starts -------------------- 

@app.route('/cusin', methods=["GET","POST"]) # End Point to Add & View the Cuisine
def cusin():
    if not settings.session.get("name"):
            return settings.redirect("/login")
    if settings.request.method=="POST":
        cuisine_name = settings.request.form["cuisine_name"]
        info=models.Cuisine(cuisine_name=cuisine_name)
        db.session.add(info)
        db.session.commit()
    fetch=models.Cuisine.query.all() 
    return settings.render_template('admin/cusin.html', getinfo=fetch)

@app.route('/cusinupdater', methods=["GET","POST"]) # End Point to Update Tax
def cusinupdater():
    if not settings.session.get("name"):
            return settings.redirect("/login")
    if settings.request.method=="POST":
        id = settings.request.form['id']
        cuisine_name = settings.request.form["cuisine_name"]
        fetch=models.Cuisine.query.filter_by(id=id).first()
        fetch.cuisine_name=cuisine_name
        db.session.commit()
        return settings.redirect("/cusin")

@app.route('/cusinupdate', methods=["GET","POST"]) # End Point to Update Tax Continued
def cusinupdate():
    if not settings.session.get("name"):
            return settings.redirect("/login")
    id = settings.request.args['id']
    fetch=models.Cuisine.query.filter_by(id=id).all()
    return settings.render_template("admin/update_cusin.html",getinfo=fetch)

@app.route('/cusindel/<int:id>', methods=["GET","POST"]) # End Point to Del the Tax
def cusindel(id):
    if not settings.session.get("name"):
            return settings.redirect("/login")
    fetch=models.Cuisine.query.filter_by(id=id).first()
    db.session.delete(fetch)
    db.session.commit()
    return settings.redirect("/cusin")

# ------------------------- Cuisine Section Ends -------------------- 
@app.route('/orders')
def order():
    return settings.render_template('front_end/orders.html')


@app.route('/checkout')
def checkout():
    return settings.render_template('front_end/checkout.html')


@app.route('/cart')
def cart():
    return settings.render_template('front_end/cart.html')


# ------------------------- Home Page Settings Starts here -------------------- ]]
@app.route('/', methods=["GET", "POST"])
def index():
    if settings.request.method== "POST":
        addition= settings.request.form['food_item'] 
        print(addition)
    fetch=models.FoodFilters.query.all() 
    return settings.render_template('front_end/index.html',fetch=fetch)


class Categories(Resource):
    def get(self):
        menu= models.MenuCategory.query.all()
        outJson = {"menu":[]}
        for m in menu:
            outJson["menu"].append(m.food_category_name)
        print(outJson)
        return jsonify(outJson)

class FoodItem(Resource):
    def get(self,category):
        menu = models.MenuCategory.query.filter_by(food_category_name=category).first()
        item=models.FoodMenuItem.query.filter_by(food_item_cat=menu.id).all()
        outjson= {"name":[],"rate":[],"img":[]}
        for i in item:
            outjson["name"].append(i.food_item_name)
            outjson["rate"].append(i.food_item_rate)
            outjson["img"].append("http://fos-testing.herokuapp.com/"+i.food_item_img)

        return jsonify(outjson)


api.add_resource(Categories, '/menu')
api.add_resource(FoodItem, '/food/<category>')

if __name__ == '__main__':
   app.run(debug=True)


