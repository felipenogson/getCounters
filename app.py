from flask import Flask, render_template, request
from getCounters import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/summoner", methods=["POST", "GET"])
def summoner():
    if request.method == "POST":
        user = {
            "summoner" : request.form['summoner'],
            "enemy" : request.form['enemy'],
            "line" : request.form['line']}
        user_champs = grab_champs(user['summoner'])
        most_used = grab_most_used(user_champs, 10)
        info = find_counters(user['enemy'], user['line'], most_used)
        return render_template('index.html', user=user, info=info)