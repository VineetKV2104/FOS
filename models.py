from settings import db

class Superlogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

class Tax(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tax_type = db.Column(db.String)
    tax_value = db.Column(db.Integer)

class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuisine_name = db.Column(db.String)

class FoodFilters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filter_name = db.Column(db.String)

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
    ingredients=db.Column(db.Integer)
    food_item_img=db.Column(db.Integer)
    food_item_cat=db.Column(db.Integer)
    food_item_filter=db.Column(db.Integer)
    food_item_cuisine=db.Column(db.Integer)

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