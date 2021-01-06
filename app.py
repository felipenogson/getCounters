from flask import Flask, render_template, request, redirect, url_for
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
            "network" : request.form['network'], 
            "enemy" : request.form['enemy'],
            "line" : request.form['line']}
        user_champs = grab_champs(user['summoner'], user['network'])
        most_used = grab_most_used(user_champs, 10)
        info, top_three, worst_three  = find_counters(user['enemy'], user['line'], most_used)
        print(user)
        return render_template('index.html', user=user, info=info, top_three=top_three, worst_three=worst_three)
    elif request.method == 'GET':
        # return '<a href="http://aws.syslinux.xyz:5000">"http://aws.syslinux.xyz:5000"</a>'
        return redirect(url_for('index'))