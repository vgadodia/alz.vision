from flask_pymongo import PyMongo
from flask import Flask, jsonify, request, send_file, render_template, redirect, url_for
import pandas as pd
# import dat


with open("clienturl.txt", "r") as x:
    app = Flask(__name__)
    app.config["MONGO_URI"] = x.read()
    client = PyMongo(app)
    db = client.db.users
    EMAIL = "a@com"


@app.route('/')
def index():
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
    jso = {"Scores" : scores, "Times" : times, "Old Sentence": sentence2, "New Sentence": sentence}
    df = pd.DataFrame(jso, columns=["Scores", "Times", "Old Sentence", "New Sentence"])
    df.to_csv("userdata.csv")
    return "Success!."


if __name__ == '__main__':
    app.run(port=5050, debug=True)
