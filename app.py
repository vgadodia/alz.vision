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
    EMAIL = ""
    loginStatus = ""
    logoutStatus = "hidden"
    tryitoutStatus = ""

# routes
@app.route('/')
def index():
    global loginStatus
    global logoutStatus
    global tryitoutStatus
    return render_template('index.html', logoutStatus=logoutStatus, loginStatus=loginStatus, tryitoutStatus=tryitoutStatus)

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
            global EMAIL 
            EMAIL = x["email"]
            print(x['name'])

            global loginStatus
            global logoutStatus
            global tryitoutStatus
            loginStatus = "hidden"
            logoutStatus = ""
            tryitoutStatus = "hidden"
            return render_template('index.html', logoutStatus=logoutStatus, loginStatus=loginStatus, tryitoutStatus=tryitoutStatus)
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
            global EMAIL
            EMAIL = username
            return redirect('/')
        else: 
            return render_template('register.html', error = "An account under that email already exists")
    return render_template('register.html', error = "") 

@app.route('/logout')
def logout():
    global EMAIL
    EMAIL = ""
    global loginStatus
    global logoutStatus
    global tryitoutStatus
    loginStatus = ""
    logoutStatus = "hidden"
    tryitoutStatus = ""
    return render_template('index.html', logoutStatus=logoutStatus, loginStatus=loginStatus, tryitoutStatus=tryitoutStatus)

@app.route('/upload')
def upload():
    global EMAIL
    if EMAIL == "":
        return render_template('uploadBlur.html', errorMessage="")
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
            print(EMAIL)
            x = db.find_one_or_404({"email": EMAIL})
            client.save_file(EMAIL + memory.filename, memory)
            x["memories"].append({"original sentence": description, "file": EMAIL +
                                  memory.filename, "time": datetime.now(), "new sentences": []})
            x = {"$set": x}
            db.update_one(db.find_one_or_404({"email": EMAIL}), x)

    return redirect("/upload")


@app.route('/image/<filename>')
def file(filename):
    return client.send_file(filename)

@app.route('/redescribe')
def redescribe():
    # print(redescription)
    global EMAIL
    if EMAIL == "":
        return render_template("redescribeBlur.html")
    image = db.find_one_or_404({"email": EMAIL})["memories"]
    for memory in image:
        if len(memory["new sentences"]) == 0:
            print(memory["file"])
            return render_template('redescribe.html', errorMessage="", image=url_for('file', filename=memory["file"]))
            # return client.send_file(NAME + memory["file"])
    # return render_template('redescription.html', image = url_for('file', filename = image[0]["file"]))
    return render_template('noRedescriptions.html')

@app.route('/redescribe', methods = ['GET', 'POST'])
def getredescription():
    # print
    print(request.method)
    if request.method == "POST":
        print("Enter POST")
        redescription = request.form['redescription']
        if redescription is "":
            image = db.find_one_or_404({"email": EMAIL})["memories"]
            for memory in image:
                if len(memory["new sentences"]) == 0:
                    print(memory["file"])
                    return render_template('redescribe.html', errorMessage="You must write a description", image=url_for('file', filename=memory["file"]))
                    # return client.send_file(NAME + memory["file"])
            # return render_template('redescription.html', image = url_for('file', filename = image[0]["file"]))
            return render_template('noRedescriptions.html')
            # return render_template('redescribe.html', errorMessage="You must write a description")
        else:
            print(redescription)
            user = db.find_one_or_404({"email": EMAIL})["memories"]
            for memory in user:
                if len(memory["new sentences"]) == 0:
                    time = datetime.now()
                    memory["new sentences"].append({"sentence": redescription, "score": main.similarity_score(
                        memory["original sentence"], redescription), "time": time})
                    break
            x = db.find_one_or_404({"email": EMAIL})
            x["memories"] = user
            x = {"$set": x}
            # print(x)
            db.update_one(db.find_one_or_404({"email": EMAIL}), x)
            # print(main.similarity_score(orig_sentence, redesc_sentence))
            # return redirect("/")
            return redirect("/redescribe")
    else:
        print("Enters this far.")
        # image = db.find_one({"name": NAME})["memories"][0]["file"] # Access a random file
        # print(image)
        image = db.find_one_or_404({"email": EMAIL})["memories"]
        for memory in image:
            if len(memory["new sentences"]) == 0:
                print(memory["file"])
                return render_template('redescribe.html', errorMessage="", image=url_for('file', filename=memory["file"]))
                # return client.send_file(NAME + memory["file"])
        # return render_template('redescription.html', image = url_for('file', filename = image[0]["file"]))
        return render_template('noRedescriptions.html')
    return render_template('noRedescriptions.html')

@app.route('/analytics')
def analytics():
    global EMAIL
    if EMAIL == "":
        return render_template("analyticsBlur.html")
    else: 
        user = db.find_one_or_404({"email": EMAIL})["memories"]
        scores = []
        times = []
        for i in user:
            sco = []
            tim = []
            newsent = i["new sentences"]
            for j in newsent:
                sco.append(j["score"])
                tim.append(round((j["time"] - i["time"]).seconds/60))
            scores.append(sco)
            times.append(tim)
        jso = {"Scores": scores, "Times": times}
        df = pd.DataFrame(jso, columns=["Scores", "Times"])
        df.to_csv("userdata.csv")
    return render_template('analytics.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
