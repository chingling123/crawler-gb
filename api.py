import flask
import re
import os
import urllib 
import json
from flask import request, json
from pymongo import MongoClient
from flask import Response

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def get_db():
    client = MongoClient('mongodb://heroku_ww1hmt25:hek3qbj1d6ed8eqcjbm4ib67ch@ds157493.mlab.com:57493/heroku_ww1hmt25')
    db = client.heroku_ww1hmt25
    return db

def extract_price(json):
    try:
        return float(json['price'])
    except KeyError:
        return 0.0

@app.route('/api/v1/planos', methods=['GET'])
def api_name():
    if 'name' in request.args:
        list = []
        name = request.args['name']
        for item in get_db().planos.find({'name': re.compile(name, re.IGNORECASE)}):
                temp = {
                    'name': item["name"],
                    'desc': item["desc"],
                    'price': item["price"]
                }
                list.append(temp)

        js = json.dumps(sorted(list, key=lambda k: k['price'], reverse=False)).encode('utf8')
        return Response(js, status=200, mimetype='application/json')
         
    if 'price' in request.args:
        list = []
        price = request.args['price']
        for item in get_db().planos.find({'price': {"$lt": float(price)}}):
                temp = {
                    'name': item["name"],
                    'desc': item["desc"],
                    'price': item["price"]
                }
                list.append(temp)

        js = json.dumps(sorted(list, key=lambda k: k['price'], reverse=False)).encode('utf8')
        return Response(js, status=200, mimetype='application/json')
    else:
        js = json.dumps({"Error": "Need name parameter"}).encode('utf8')
        return Response(js, status=200, mimetype='application/json')
    
    
@app.route('/api/v1/planos', methods=['POST'])
def api_add():
    req_data = request.get_json()
    msg = ''
    try:
        for item in req_data:
            r = get_db().planos.find({'price': float(item["price"]), 'desc': item["desc"], 'name': item["name"], 'gb': item["gb"]})
            if r.count() == 0:
                get_db().planos.insert(item)
        msg = "added"
    except pymongo.errors.ConnectionFailure as e:
        msg = "Database error: %s" % e
    finally:
        return msg

port = int(os.environ.get("PORT", 80))
app.run(host='0.0.0.0', port=port)