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



app = Flask(__name__)


NAME = "GenericUser"

# routes
@app.route('/')
def index():
    '''
    TODO: Some sort of login system. For now, I'll have it default.
    '''
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html') 

@app.route('/register')
def register():
    return render_template('register.html') 

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
