import pandas as pd
from pandas import Series, DataFrame
import flask
import re
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import io
import time
import requests
import matplotlib

matplotlib.use('Agg')

app = Flask(__name__)
# df = pd.read_csv("main.csv")

COUNT = 0
COUNT_INDEX = 0
COUNT_INDEX2 = 0
last_visit = 0


@app.route("/donate.html")
def money():
    global COUNT_INDEX
    global COUNT_INDEX2
    with open("donate.html") as f:
        html = f.read()
        links = str(request.url)
        with open("link.txt", "a") as f1:
            lin = f1.write(links + "\n")
        capital = re.findall(r"[A-Z]", links)
        if len(capital) == 1:
            if capital[0] == "A":
                COUNT_INDEX += 1
            else:
                COUNT_INDEX2 += 1
    return html


@app.route('/')
def increment_1():
    global COUNT
    global COUNT_INDEX
    global COUNT_INDEX2
    if COUNT <= 9:
        # print(COUNT)
        if COUNT % 2 == 0:
            with open("index.html") as f3:
                html3 = f3.read()
                COUNT += 1
            return html3
        else:
            with open("index2.html") as f4:
                html4 = f4.read()
                COUNT += 1
            return html4
    else:
        if COUNT_INDEX > COUNT_INDEX2:
            with open("index.html") as f3:
                html3 = f3.read()
            return html3
        else:
            with open("index2.html") as f4:
                html4 = f4.read()
            return html4


@app.route("/browse.html")
def table():
    with open("browse.html") as f:
        page = f.read()
        data = pd.read_csv("main1.csv", encoding="utf-8")
    page = page.replace("browse", data.to_html())
    return page


remote_address = []


@app.route("/browse.json")
def json_table():
    global last_visit
    # with open("browse.json") as f:
    #     page=f.read()
    data = pd.read_csv("main1.csv", encoding="utf-8")
    dict_data = data.to_dict(orient="index")
    # page = page.replace("browse",data.to_json())
    f1 = flask.request.remote_addr
    with open("visitor.txt", "a") as f:
        f.write(f1 + "\n")  # 2
    if f1 not in remote_address:
        remote_address.append(f1)
        last_visit = time.time()
        return jsonify(dict_data)
    else:
        if time.time() - last_visit > 60:
            last_visit = time.time()
            return jsonify(dict_data)
        return flask.Response("<b>go away</b>",
                              status=429,
                              headers={"Retry-After": "3"})


@app.route('/mt.jpg')
def plot1():
    fig, ax = plt.subplots(figsize=(3, 2))
    with open("mt.jpg", "wb") as f:
        fig.savefig(f)
    with open("mt.jpg", "rb") as f:
        return f.read()


@app.route("/dashboard_1.svg")
def fei1():
    fig, ax = plt.subplots(figsize=(3, 2))
    data = pd.read_csv("main1.csv", encoding="utf-8")
    pd.Series(data["转发"]).plot.line(ax=ax)
    ax.set_ylabel("REPOST")
    plt.tight_layout()

    f = io.StringIO()
    fig.savefig(f, format="svg")
    plt.close()
    return flask.Response(f.getvalue(),
                          headers={"Content-Type": "image/svg+xml"})


@app.route("/dashboard_2.svg")
def fei2():
    fig, ax = plt.subplots(figsize=(3, 2))
    data = pd.read_csv("main1.csv", encoding="utf-8")
    pd.Series(data["评论"]).plot.line(ax=ax)
    ax.set_ylabel("COMMENT")
    plt.tight_layout()
    f = io.StringIO()
    fig.savefig(f, format="svg")
    plt.close()
    return flask.Response(f.getvalue(),
                          headers={"Content-Type": "image/svg+xml"})


@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if len(re.findall(r"^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-z0-9_-]+\.[a-z0-9_-]{3}$", email)) > 0:
        with open("emails.txt", "a") as f:
            f.write(email + "\n")  # 2
            num_subscribed = len(open("emails.txt").readlines()) + 1
        #    num_subscribed = app.json.response
        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    return jsonify(f"INVALID EMAIL!!!")  # 3


@app.route('/vote', methods=["POST"])
def vote():
    vote = str(request.data, "utf-8")
    if len(re.findall(r"[0-5]", vote)) > 0:
        with open("vote.txt", "a") as f:
            f.write(vote + "\n")  # 2
            num_vote = len(open("vote.txt").readlines()) + 1
        #    num_subscribed = app.json.response
        return jsonify(f"thanks, you're voter number {num_vote}!")
    return jsonify(f"地主家也没有余粮了....")  # 3


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False)
