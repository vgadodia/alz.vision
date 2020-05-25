'''
I'm trying to use this: https://flask-pymongo.readthedocs.io/en/latest/
'''

import pandas as pd
from flask import Flask, jsonify, request, send_file, render_template, redirect, url_for
import mainModel
import numpy as np
import matplotlib.pyplot as plt 
import sklearn
import main
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
    # main_client = pymongo.MongoClient(x.read())

# print(os.path.dirname())

# print(client.list_database_names())
db = client.db.users
beta_db = client.db.photos

NAME = "GenericUser"

# routes
@app.route('/')
def index():
    '''
    TODO: Some sort of login system. For now, I'll have it default.
    '''
    login = True
    # NAME = "New User"
    if login:
        user = {"name": NAME, "memories": []}
        x = db.insert_one(user)
    return render_template('index.html', text="")

@app.route('/upload')
def upload():
    return render_template('upload.html', text="") 

@app.route('/upload', methods = ['GET', 'POST'])
def uploadimage():
    if request.method == "POST":
        text = request.form['text']
        memory = request.files['memory']
        if text is "":
            print("You must write a description")
            return render_template('upload.html', text="You must write a description")
        elif memory.filename == "":
            print("You must upload a photo")
            return render_template('upload.html', text="You must upload a photo")
        else:
            x = db.find_one_or_404({"name": NAME})
            print(x)
            print(NAME)
            print(text)
            client.save_file(NAME + memory.filename, memory)
            x["memories"].append({"original sentence": text, "file": NAME + memory.filename, "time": datetime.now(), "new sentences": []})
            x = {"$set": x}
            db.update_one(db.find_one_or_404({"name": NAME}), x)
            # mongo.save_file(filename, x["memories"]["file"])
            '''
            TODO: We're going to need to create a new collection for each user?
                  Because I think save_filename just works for saving it to the collection.
            '''
            print(text)
            print(memory.filename)
    return redirect("/upload")

# @app.route('/redescription')
# def redescription():
#     return render_template("redescription.html")

@app.route('/image/<filename>')
def file(filename):
    return client.send_file(filename)

@app.route('/redescription', methods = ['GET', 'POST'])
def getredescription():
    if request.method == "POST":
        redescription = request.form['redescription']
        if redescription is "":
            print("You must write a description")
        else:
            print(redescription)
            user = db.find_one_or_404({"name": NAME})["memories"]
            for memory in user:
                if len(memory["new sentences"]) == 0:
                    time = datetime.now()
                    memory["new sentences"].append({"sentence": redescription, "score": main.similarity_score(memory["original sentence"], redescription), "time": time})
                    break
                    # x = db.find_one_or_404({"name": NAME})
                    # print("ENTER STUFF")
                    # print(x, NAME)
                    # time = 0
                    # x["memories"][0]["new sentences"].append({"sentence": redescription, "score": main.similarity_score(orig_sentence, redescription), "time": time})
            x = db.find_one_or_404({"name": NAME})
            x["memories"] = user
            x = {"$set": x}
            print(x)
            db.update_one(db.find_one_or_404({"name": NAME}), x)
            # print(main.similarity_score(orig_sentence, redesc_sentence))
            # return redirect("/")
            return redirect("/redescription")
    if request.method == "GET":
        # image = db.find_one({"name": NAME})["memories"][0]["file"] # Access a random file
        # print(image)
        image = db.find_one_or_404({"name": NAME})["memories"]
        for memory in image:
            if len(memory["new sentences"]) == 0:
                print(memory["file"])
                return render_template('redescription.html', image=url_for('file', filename = memory["file"]))
                # return client.send_file(NAME + memory["file"])
        # return render_template('redescription.html', image = url_for('file', filename = image[0]["file"]))
        return render_template('404.html')

@app.route('/redescription')
def redescription():
    image = db.find_one_or_404({"name": NAME})["memories"]
    for memory in image:
        if len(memory["new sentences"]) == 0:
            print(memory["file"])
            return render_template('redescription.html', image=url_for('file', filename = memory["file"]))
            # return client.send_file(NAME + memory["file"])
    return render_template('redescription.html', image = url_for('file', filename = memory["file"]))

@app.route('/analytics')
def redescribe():
    return render_template('analytics.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
