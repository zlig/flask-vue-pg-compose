#!/usr/bin/env python
from flask import Flask, render_template, jsonify
from redis import Redis

app = Flask(__name__)
redis = Redis(host='info-redis', port=6379)

@app.route("/")
@app.route("/hello")
def index():
    return render_template('index.html')

@app.route("/hi")
@app.route("/hi/<name>")
def hi(name=None):
    if name:
        return jsonify({"data": "hi, %s" % name}), 200
    else:
        return jsonify({"data": "hi"}), 200

@app.route("/ping")
def ping():
    return jsonify({"response": "pong"}), 200

@app.route('/redis')
def hello():
    redis.incr('hits')
    views = int.from_bytes(redis.get('hits'))
    print('Redis views: %d' % views, flush=True)
    return jsonify({"data": str(views)}), 200

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"data": "not found", "error": "resource not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
