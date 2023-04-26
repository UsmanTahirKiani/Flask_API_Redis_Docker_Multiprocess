import flask
from flask import request, jsonify
import sqlite3
import time
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Twitter API</h1>
<p></p>'''


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.errorhandler(500)
def server_error(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 500


@app.route('/api/v1/three', methods=['GET'])
def api_filter1():
    results = 3
    return jsonify(results)


@app.route('/api/v1/two', methods=['GET'])
def api_filter():
    time.sleep(20)
    results = 2
    return jsonify(results)

