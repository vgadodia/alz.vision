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
from graphs import svr, bar_graph, random_forest, expected_value, svr_overtime, rf_overtime
from letsGo import analyse

with open("clienturl.txt", "r") as x:
    app = Flask(__name__)
    app.config["MONGO_URI"] = x.read()
    client = PyMongo(app)
    db = client.db.users
    EMAIL = ""
    loginStatus = ""
    logoutStatus = "hidden"
    tryitoutStatus = ""
    welcomeStatus = "hidden"
    welcomeName = ""

# routes


@app.route('/')
def index():
    global loginStatus
    global logoutStatus
    global tryitoutStatus
    global welcomeStatus
    global welcomeName
    return render_template('index.html', logoutStatus=logoutStatus, loginStatus=loginStatus, tryitoutStatus=tryitoutStatus, welcomeStatus=welcomeStatus, welcomeName=welcomeName)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password'].encode('utf-8')
        x = db.find_one(
            {"email": username, "password": hashlib.sha224(password).hexdigest()})
        if x == None:
            return render_template('login.html', error="Invalid Credentials. Try again or sign up!")
        else:
            global EMAIL
            EMAIL = x["email"]

            global loginStatus
            global logoutStatus
            global tryitoutStatus
            global welcomeStatus
            global welcomeName
            loginStatus = "hidden"
            logoutStatus = ""
            tryitoutStatus = "hidden"
            welcomeStatus = ""
            welcomeName = x['name'].split()
            welcomeName = welcomeName[0]
            return render_template('index.html', logoutStatus=logoutStatus, loginStatus=loginStatus, tryitoutStatus=tryitoutStatus, welcomeStatus=welcomeStatus, welcomeName=welcomeName)
    return render_template('login.html', error="")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['email']
        password = request.form['password'].encode('utf-8')
        print(name, username, password)
        x = db.find_one({"email": username})
        if x == None:
            user = {"name": name, "password": hashlib.sha224(
                password).hexdigest(), "email": username, "memories": []}
            x = db.insert_one(user)
            global EMAIL
            EMAIL = username

            global loginStatus
            global logoutStatus
            global tryitoutStatus
            global welcomeStatus
            global welcomeName
            loginStatus = "hidden"
            logoutStatus = ""
            tryitoutStatus = "hidden"
            welcomeStatus = ""
            welcomeName = name.split()
            welcomeName = welcomeName[0]
            return render_template('index.html', logoutStatus=logoutStatus, loginStatus=loginStatus, tryitoutStatus=tryitoutStatus, welcomeStatus=welcomeStatus, welcomeName=welcomeName)
        else:
            return render_template('register.html', error="An account under that email already exists")
    return render_template('register.html', error="")


@app.route('/logout')
def logout():
    global EMAIL
    EMAIL = ""
    global loginStatus
    global logoutStatus
    global tryitoutStatus
    global welcomeStatus
    global welcomeName
    loginStatus = ""
    logoutStatus = "hidden"
    tryitoutStatus = ""
    welcomeStatus = "hidden"
    print("Logging out")
    return render_template('index.html', logoutStatus=logoutStatus, loginStatus=loginStatus, tryitoutStatus=tryitoutStatus, welcomeStatus=welcomeStatus, welcomeName=welcomeName)


@app.route('/upload')
def upload():
    global EMAIL
    if EMAIL == "":
        return render_template('uploadBlur.html', errorMessage="")
    return render_template('upload.html', errorMessage="")


@app.route('/upload', methods=['GET', 'POST'])
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


@app.route('/redescribe', methods=['GET', 'POST'])
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
        return render_template("analyticsBlur.html", displayStatus="visible")
    else:
        user = db.find_one_or_404({"email": EMAIL})["memories"]
        scores = []
        times = []
        sentence = []
        sentence2 = []
        for i in user:
            sco = []
            tim = []
            sent = []
            sent2 = []
            newsent = i["new sentences"]
            for j in newsent:
                sco.append(j["score"])
                tim.append(round((j["time"] - i["time"]).seconds/60))
                sent.append(j["sentence"])
                sent2.append(i["original sentence"])
            scores.append(sco)
            times.append(tim)
            sentence.append(sent)
            sentence2.append(sent2)
        # jso = {"Scores" : scores, "Times" : times, "Old Sentence": sentence2, "New Sentence": sentence}
        # df = pd.DataFrame(jso, columns=["Scores", "Times", "Old Sentence", "New Sentence"])
        # df.to_csv("userdata.csv")

        # jso = {"Scores": scores, "Times": times}
        # df = pd.DataFrame(jso, columns=["Scores", "Times"])
        # df.to_csv("userdata.csv")

        print(scores)
        print(times)

        if len(scores) == 0 or len(scores) == 1:
            return render_template('analyticsNone.html')

        id_memory = [[i] for i in range(1, len(scores)+1)]
        memory_vs_time = svr_overtime(id_memory, scores)
        memory_vs_time = memory_vs_time.decode("utf-8")

        memory_vs_time_rf = rf_overtime(id_memory, scores)
        memory_vs_time_rf = memory_vs_time_rf.decode("utf-8")
        

        svr_img = svr(times, scores)
        randomforest_img = random_forest(times, scores)
        bargraph_img = bar_graph(times, scores)
        cluster_imgs = analyse()
        exp_val = expected_value(scores)
        cl1 = cluster_imgs[0].decode("utf-8")
        cl2 = cluster_imgs[1].decode("utf-8")
        cl3 = cluster_imgs[2].decode("utf-8")
        perfect_rate = cluster_imgs[3]
        forget_rate = cluster_imgs[4]
        type_rate = cluster_imgs[5]
        svr_img = svr_img.decode("utf-8")
        randomforest_img = randomforest_img.decode("utf-8")
        bargraph_img = bargraph_img.decode("utf-8")

        if len(scores) <= 10:
            return render_template('analyticsLess.html', memory_vs_time_rf=memory_vs_time_rf, memory_vs_time=memory_vs_time, exp_val=exp_val, svr_img=svr_img, randomforest_img=randomforest_img, bargraph_img=bargraph_img)

        return render_template('analytics.html', memory_vs_time_rf=memory_vs_time_rf, memory_vs_time=memory_vs_time, exp_val=exp_val, perfect_rate=perfect_rate, forget_rate=forget_rate, type_rate=type_rate, cl1=cl1, cl2=cl2, cl3=cl3, svr_img=svr_img, randomforest_img=randomforest_img, bargraph_img=bargraph_img)
    return render_template('analytics.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)
