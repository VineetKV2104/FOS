import settings

from settings import app, db

import models

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

# ------------------------- Food Menu Category Section Ends -------------------- 

# ------------------------- Ingredient Category Section Starts -------------------- 



# ------------------------- Ingredient Category Section Ends -------------------- 


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
    return settings.render_template('front_end/index.html')




if __name__ == '__main__':
   app.run(debug=True)


