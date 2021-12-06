from flask import Flask, request, render_template, redirect, session
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from flask_session import Session


app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fos.db' 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQLAlchemy(app)