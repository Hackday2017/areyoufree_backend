from . import api
from flask import request, jsonify

import redis
import pickle

@api.route('/gettime/', methods = ['POST'])
def gettime():
    if request.method == 'POST':
        groupname = request.get_json().get("groupname")
        
        conn = redis.StrictRedis(host='localhost', decode_responses=True, port=6379, db=6)
        keys = conn.keys()
        #不存在返回404
        if keys == None:
            return jsonify({}),404

        dic = {}
        for k in keys:
            ak = pickle.loads(k)
            if ak[1] == groupname:
                dic[ak[0]] = eval(pickle.loads(conn.get(str(k))))

        ret = {}
        baseint = 0
        daykey = pickle.loads(keys[0])
        date = daykey[2]

        for i in range(7):
            datetmp = str(int(date) + i)
            datetmp = legaldate(datetmp)
            ret[datetmp] = {}
            hour = 0

            for j in range(48):
                hour = j
                hourdic = {}
                ret[datetmp][hour] = hourdic
                
                ret[datetmp][hour]["member"] = []
                ret[datetmp][hour]["member_count"] = 0
                
                dickeys = list(dic.keys())

                for k in range(len(dickeys)):
                    name = dickeys[k]
                    print("node now:" , baseint+hour, " value", dic[name][baseint+hour], " type:", type(dic[name][baseint+hour]))
                    if dic[name][baseint + hour]:
                        ret[datetmp][hour]["member"].append(name)
                        ret[datetmp][hour]["member_count"] += 1

            baseint += 48
        
        return jsonify(ret), 200
        
def legaldate(date):
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    year = int(year)
    month = int(month)
    day = int(day)


    if month == 2:
        if (year%100 == 0 and year%400 == 0) or (year%100!=0 and year % 4 == 0):
            if day > 29:
                day -= 29
                month += 1
        else:
            if day > 28:
                day -= 28
                month += 1

    elif month == 12:
        if day > 31:
            day -= 31
            month -= 11
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
        day = "0" + str(day)
    else:
        day = str(day)
    
    return str(year)+ str(month) + str(day)
