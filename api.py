import flask
import re
from flask import request, json
from pymongo import MongoClient

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def get_db():
    client = MongoClient('https://api.mlab.com/api/1/databases?apiKey=K4oOFvyQiC5Dkup6ULBPneykGOc1gTfm')
    db = client.planos
    return db

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
        return json.dumps(list)
    else:
        return json.dumps({"Error": "Need name parameter"})
    
    
@app.route('/api/v1/planos', methods=['POST'])
def api_add():
    req_data = request.get_json()
    msg = ''
    try:
        get_db().planos.insert(req_data)
        msg = "added"
    except pymongo.errors.ConnectionFailure as e:
        msg = "Database error: %s" % e
    finally:
        return msg

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)