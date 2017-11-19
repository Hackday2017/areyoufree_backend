from . import api
from flask import request, jsonify

import redis
import pickle

@api.route('/givetime/', methods = ['POST'])
def givetime():
    if request.method == 'POST':
        username = request.get_json().get("username")
        groupname = request.get_json().get("groupname")
        start_date = request.get_json().get("start_date")
        hour = request.get_json().get("time")

        conn = redis.StrictRedis(host='localhost',decode_responses=True, port=6379, db=7)
        
        t = [username, groupname, start_date]
        identify = conn.get(str(t))
        #identify = conn.get(str(pickle.dumps(t)))
        if identify == None:
            conn.set(str(t), str(hour))
            return jsonify({}),200
        else:
            return jsonify({}),403
