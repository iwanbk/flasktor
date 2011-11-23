import hashlib

from flask import Flask
from flask import render_template
from flask import request
from werkzeug.wrappers import Request
from flask import g
from flask import globals

app = Flask(__name__)

globals.db = {}

_DEBUG_ON = False
_INTERVAL = 1800
_INTERVAL_MIN = 300
_CLIENT_TIMEOUT = 60
_NO_PEER_ID = True
_NO_SEED_P2P = True
_ENABLE_SHORT_ANNOUNCE = True

def is_seed(request):
    left = request.args.get("left")
    
    if left == None:
        return False
    
    if left == 0:
        return True
    
    return False
def track(dict, request, interval = 60, min_ival = 0):
    p = ""
    c = 0
    i = 0
    
    for k,d in dict.iteritems():
        if d[7] != 0:
            c = c + 1
            if (_NO_SEED_P2P and is_seed(request) == True):
                continue
        else:
            i = i + 1
        
        #do some bencoding
        pid = ""
        if request.args.get("no_peer_id") == None and _NO_PEER_ID == True:
            pid = "7:peer id" + str(len(d[1])) + ":" + d[1]
        
        p = p + 'd2:ip' + str(len(d[0])) + ':' + d[0] + pid + '4:porti' + d[2] + 'ee'
    
    r = 'd8:intervali' + str(interval) + 'e12:min intervali' + str(min_ival) + 'e8:completei' + str(c) + 'e10:incompletei' + str(i) + 'e5:peersl' + p + 'ee'
    
    return r


interval = _INTERVAL
interval_min = _INTERVAL_MIN
'''
@app.route("/announce/scrape",methods = ["GET"])
def scrape_handler():
    print " ===== SCRAPE ========="
    return "failed"
'''
@app.route("/announce/",methods = ["GET"])
def announce_handler():
    if request.args.get("short") != None and _ENABLE_SHORT_ANNOUNCE == True:
        interval = 120
        interval_min = 30
    
    args_info_hash_utf8 = request.args.get("info_hash").decode()
    args_peer_id_utf8 = request.args.get("peer_id").decode()
    
    to_hash =  args_peer_id_utf8.encode("utf-8") + args_info_hash_utf8.encode("utf-8")
    
    sum = hashlib.sha1(to_hash)
    
    #When should we remove the client?
    #$expire = time()+$interval;
    expire = 200 #TODO
    
    if sum in globals.db:
        if globals.db[sum][6] != request.args.get("key"):
            print "auth failed"
            sleep(3)
            return ""
        
    db_val = []
    db_val.append(request.remote_addr)
    db_val.append(request.args.get("peer_id"))
    db_val.append(request.args.get("port"))
    db_val.append(expire)
    db_val.append(args_info_hash_utf8)
    user_agent = "sesuatu" #TODO
    db_val.append(user_agent)
    db_val.append(request.args.get("key"))
    db_val.append(is_seed(request))
    
    print "===db val === "
    print db_val
    print "end db vall"
    
    globals.db[sum] = db_val
    
    if request.args.get("event") == "stopped":
        del globals.db[sum]
        return track([], request)
    
    #cek if any client timeout
    for d in globals.db.iteritems():
        pass
    
    #save client list
    
    #build reply
    reply_dict = {}
    for k,v in globals.db.iteritems():
        print v
        if v[4] == args_info_hash_utf8:
            reply_dict[k] = v
    
    del reply_dict[sum]
    
    return track(reply_dict, request)    
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)