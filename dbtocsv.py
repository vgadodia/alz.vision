from flask_pymongo import PyMongo
from flask import Flask, jsonify, request, send_file, render_template, redirect, url_for
import pandas as pd


with open("clienturl.txt", "r") as x:
    app = Flask(__name__)
    app.config["MONGO_URI"] = x.read()
    client = PyMongo(app)
    db = client.db.users
    EMAIL = "name@name.com"


@app.route('/')
def index():
    user = db.find_one_or_404({"email": EMAIL})["memories"]
    scores = []
    times = []
    for i in user:
        sco = []
        tim = []
        newsent = i["new sentences"]
        for j in newsent:
            sco.append(j["score"])
            tim.append(j["time"] - i["time"])
        scores.append(sco)
        times.append(tim)
    jso = {"Scores" : scores, "Times" : times}
    df = pd.DataFrame(jso, columns=["Scores", "Times"])
    df.to_csv("userdata.csv")
    return "Success!."


if __name__ == '__main__':
    app.run(port=5000, debug=True)