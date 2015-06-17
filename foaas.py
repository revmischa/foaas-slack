#!/usr/bin/env python

from flask import Flask
import requests

app = Flask(__name__)

@app.route('/fuckoff/<name>')
def fuckoff(name):
	return "webhook response for %s" % name

if __name__ == '__main__':
	app.run(host='0.0.0.0')