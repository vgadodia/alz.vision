'''
I'm trying to use this: https://flask-pymongo.readthedocs.io/en/latest/
'''

import pandas as pd
from flask import Flask, jsonify, request, send_file, render_template, redirect, url_for
import dataAnalysis
import numpy as np
import matplotlib.pyplot as plt 
import sklearn
import similarity.main
from flask_pymongo import PyMongo
import pymongo
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import pathlib
# print(str(pathlib.Path(__file__).parent.absolute()) + "/static/")


# app
# app = Flask(__name__)

with open("clienturl.txt", "r") as x: 
    # print(x.read())
    app = Flask(__name__)
    app.config["MONGO_URI"] = x.read()
    client = PyMongo(app)

db = client.db.users

print(db.getUsers())