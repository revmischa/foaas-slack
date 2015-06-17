#!/usr/bin/env python

from flask import Flask, request
import requests
import json
import re
import random

app = Flask(__name__)

@app.route('/fuckoff')
def fuckoff():
	name_from = request.values.get('username')
	text = request.values.get('text')

	name = re.sub(r"(?i)^fuckoff\s*", "", text)

	ops_r = requests.get('http://foaas.com/operations')
	ops = json.loads(ops_r.text)

	# assemble list of valid ops
	if not name:
		# if we don't have a target name then we need to skip items that have a name param
		ops = [ op for op in ops if len([ field for field in op['fields'] if field['field'] == 'name' ]) ]

#	ops = [ op for op in ops if len([ field for field in op['fields'] if field['field'] == 'name' ])

	# pick random op
	op = random.choice(ops)

	print op
	url = op['url']

	if name_from:
		url = url.replace(':from', name_from)

	if name:
		url = url.replace(':name', name)

	# get fuckoff
	fo_r = requests.get('http://foaas.com%s' % url, headers={ 'Accept': 'application/json' })
	fo = json.loads(fo_r.text)

	# slack response
	res_text = fo['message'] + "\n_" + fo['subtitle'] + '_'
	resp = {
		'text': res_text
	}

	return json.dumps(resp)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)