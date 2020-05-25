'''
I'm trying to use this: https://flask-pymongo.readthedocs.io/en/latest/
'''

import pandas as pd
from flask import Flask, jsonify, request, send_file, render_template, redirect, url_for
import dataAnalysis
import numpy as np
import matplotlib.pyplot as plt 
import sklearn
from similarity import main
from flask_pymongo import PyMongo
import pymongo
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import pathlib
import hashlib

with open("clienturl.txt", "r") as x:
    app = Flask(__name__)
    app.config["MONGO_URI"] = x.read()
    client = PyMongo(app)
    db = client.db.users
    NAME = ""

# routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password'].encode('utf-8')
        x = db.find_one(
            {"email": username, "password": hashlib.sha224(password).hexdigest()})
        if x == None:
            return render_template('login.html', error = "Invalid Credentials. Try again or sign up!")
        else:
            global NAME 
            NAME = x["name"]
            return render_template('index.html')
    return render_template('login.html', error = "") 

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['email']
        password = request.form['password'].encode('utf-8')
        print(name, username, password)
        x = db.find_one({"email": username})
        if x == None:
            user = {"name": name, "password": hashlib.sha224(password).hexdigest(), "email": username, "memories": []}
            x = db.insert_one(user)
            global NAME
            NAME = name
            return render_template('index.html')
        else: 
            render_template('register.html', error = "An account under that email already exists")
    return render_template('register.html', error = "") 

@app.route('/upload')
def upload():
    return render_template('upload.html', errorMessage="") 

@app.route('/upload', methods = ['GET', 'POST'])
def getupload():
    if request.method == "POST":
        description = request.form['description']
        memory = request.files['memory']
        if memory.filename == "":
            return render_template('upload.html', errorMessage="You must upload a photo")
        elif description is "":
            return render_template('upload.html', errorMessage="You must write a description")
        else:
            print(description)
            print(memory.filename)
    return redirect("/upload")


# @app.route('/image/<filename>')
# def file(filename):
#     return client.send_file(filename)

@app.route('/redescribe')
def redescribe():
    return render_template('redescribe.html', errorMessage="")

@app.route('/redescribe', methods = ['GET', 'POST'])
def getredescription():
    if request.method == "POST":
        redescription = request.form['redescription']
        if redescription is "":
            return render_template('redescribe.html', errorMessage="You must write a description")
        else:
            print(redescription)
    return redirect("/redescribe")

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
