#!/usr/bin/env python

from flask import Flask, request
import requests
import json
import re
import random

app = Flask(__name__)


@app.route('/fuckoff_slashcommand', methods=['GET', 'POST'])
def slashcommand():
    fo = gen_fuckoff()
    return {
        "response_type": "in_channel",
        "attachments": [{
            'title': fo['subtitle'],
            'fallback': fo['message'],
            'text': fo['message'],
            'parse': 'none',
            'mrkdwn_in': []
        }]
    }

@app.route('/fuckoff', methods=['GET', 'POST'])
def webhook():
    fo = gen_fuckoff()
    res_text = fo['message'] + "\n_" + fo['subtitle'] + '_'
    resp = {
        'text': res_text
    }

    return json.dumps(resp)

def gen_fuckoff():
    # trigger warning: trigger word
    trigger_word = request.values.get('trigger_word')

    # from/dest params
    name_from = request.values.get('user_name')
    text = request.values.get('text')

    # strip trigger word
    name = re.sub(r"(?i)^%s\s*" % trigger_word, "", text)

    # grab available fuckoff operateions
    ops_r = requests.get('http://foaas.com/operations')
    ops = json.loads(ops_r.text)

    # assemble list of valid ops
    if not name:
        # if we don't have a target name then we need to skip items that have a name param
        ops = [ op for op in ops if len([ field for field in op['fields'] if field['field'] == 'name' ]) ]

    # strip out operations that require extra fields
    basic_ops = []
    for op in ops:
        fields = op['fields']
        field_names = [field['field'] for field in fields]
        # if not len(field_names) or set(field_names) == set(['from']) or set(field_names) == set(['name', 'from']):

        # only allow ones with from/to
        if set(field_names) == set(['name', 'from']):
            basic_ops.append(op)

    # pick random op
    op = random.choice(basic_ops)

    url = op['url']

    if name_from:
        url = url.replace(':from', name_from)

    if name:
        url = url.replace(':name', name)

    # get fuckoff
    fo_r = requests.get('http://foaas.com%s' % url, headers={ 'Accept': 'application/json' })
    fo = json.loads(fo_r.text)
    return fo

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)