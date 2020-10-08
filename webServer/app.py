# from flask import Flask
# app = Flask(__name__)
#
# @app.route('/')
# def hello():
#     return 'Welcome to My Watchlist!'

from flask import Flask, render_template, jsonify, request
import os
app = Flask(__name__)



nextdict = {}
predict = {}


# replace with data base in the future
def buildDict():
    ids = os.listdir("../contentServer/dash/data/")

    print(ids[0])

    nlen = len(ids)

    for i in range(nlen):
        idxi = i
        idxj = (i+1) % nlen


        nextdict[ids[idxi]] = ids[idxj]

        predict[ids[idxj]] = ids[idxi]

buildDict()

def getNext(vid):
    return nextdict[vid]

def getPre(vid):
    return predict[vid]

@app.route('/json1')
def json():
    return render_template('json.html')


@app.route('/svs')
def svs():
    return render_template('index.html')

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return jsonify(username="zhuqi")


# #background process happening without any refreshing
# @app.route('/postmethod')
# def postmethod():
#     print (jsonify(username="uid"))
#     return jsonify(username="zhuqi")

@app.route('/postmethod')
def postmethod():
    jsdata = request.args.get('vid', 0, type=str)
    return jsonify(result="server: "+ jsdata)

@app.route('/getnext')
def getnext():
    jsdata = request.args.get('vid', 0, type=str)
    return jsonify(result=getNext(jsdata))

@app.route('/getpre')
def getpre():
    jsdata = request.args.get('vid', 0, type=str)
    return jsonify(result=getPre(jsdata))