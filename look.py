from flask_pymongo import PyMongo
from flask import Flask, jsonify, request, send_file, render_template, redirect, url_for
import pandas as pd
# import dat


with open("clienturl.txt", "r") as x:
    app = Flask(__name__)
    app.config["MONGO_URI"] = x.read()
    client = PyMongo(app)
    db = client.db.users
    EMAIL = "name@name.com"


@app.route('/')
def index():
    user = db.find()
    scores = []
    times = []
    for i in user:
        print(i)
        scores.append(i["name"])
        try:
            times.append(i["email"])
        except:
            times.append("")
    jso = {"Name": scores, "Email": times}
    df = pd.DataFrame(jso, columns=["Name", "Email"])
    df.to_csv("users.csv")
    return "Success!."


if __name__ == '__main__':
    app.run(port=5000, debug=True)
