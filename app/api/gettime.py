from . import api
from flask import request, jsonify

import redis
import json

@api.route('/gettime/', methods = ['POST'])
def gettime():
    if request.method == 'POST':
        groupname = request.get_json().get("groupname")

        conn = redis.StrictRedis(host='localhost',decode_responses=True, port=6379, db=5)
        keys = list(conn.keys())
        

        #不存在返回404
        if keys == None:
            return jsonify({}),404

        dic = {}
        for k in keys:
            if json.loads(k[1]) == groupname:
                dic[json.loads(k[0])] = json.loads(conn.get(k))

        ret = {}
        baseint = 0
        date = list(keys[0][2])
        print(date)
        input(">")
        for i in range(7):
            date = legaldate(str(int(date)+i))
            datedic = {}
            ret[date] = datedic
            hour = 0

            for j in range(48):
                hour = j
                hourdic = {}
                ret[date][hour] = hourdic
                
                ret[date][hour]["member"] = []
                ret[date][hour]["member_count"] = 0
                
                dickeys = dic.keys()

                for k in range(len(dickeys)):
                    name = dickeys[k]
                    if dic[name][baseint + hour]:
                        ret[date][hour]["member"].append(name)
                        ret[date][hour]["member_count"] += 1

            baseint += 48
        
        return jsonify(ret), 200
        
def legaldate(date):
    year = date[0:4]
    print(year)
    month = date[4:6]
    print(month)
    day = date[6:8]
    print(day)
    year = int(year)
    month = int(month)
    day = int(day)

    if month == 2:
        if (year%100 == 0 and year%400 == 0) or (year%100!=0 and year % 4 == 0):
            if day >= 29:
                day -= 29
                month += 1
    
    elif month == 12:
        if day > 31:
            day -= 31
            month -= 12
            year += 1

    elif month in [1, 3, 5, 7, 8, 10]:
        if day > 31:
            day -= 31
            month += 1
    
    else:
        if day > 30:
            day -= 30
            month += 1

    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)

    if day < 10:
        day = "0" + str(month)
    else:
        day = str(day)

    return year+month+day
