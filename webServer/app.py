# from flask import Flask
# app = Flask(__name__)
#
# @app.route('/')
# def hello():
#     return 'Welcome to My Watchlist!'

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
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