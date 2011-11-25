import re

from flask import Flask
from flask import render_template
from flask import request
from werkzeug.wrappers import Request
from flask import g
from flask import globals

app = Flask(__name__)

globals.db = {}
globals.trackdb = {}

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
    c = 0
    i = 0
    p = ""
    
    for k,d in dict.iteritems():
        if d['is_seed'] == True:
            c = c + 1
            if (_NO_SEED_P2P and is_seed(request) == True):
                continue
        else:
            i = i + 1
        
        #do some bencoding
        #if request.args.get("no_peer_id") == None and _NO_PEER_ID == True:
        #pid = "7:peer id" + str(len(d['peer_id'])) + ":" + d['peer_id']
        pid = ""
        
        p = 'd2:ip' + str(len(d['ip'])) + ':' + d['ip'] + pid + '4:porti' + d['port'] + 'ee'
        #p = pid + 'd2:ip' + str(len(d['ip'])) + ':' + d['ip'] + '4:porti' + d['port'] + 'ee'
    
    r = 'd8:intervali' + str(interval) + 'e12:min intervali' + str(min_ival) + 'e8:completei' + str(c) + 'e10:incompletei' + str(i) + 'e5:peersl' + p + 'ee'
    
    print r
    return r


interval = _INTERVAL
interval_min = _INTERVAL_MIN
'''
@app.route("/announce/scrape",methods = ["GET"])
def scrape_handler():
    print " ===== SCRAPE ========="
    return "failed"
'''
def add_to_db(info_hash,val):
    if info_hash not in globals.db:
        globals.trackdb[info_hash] = []
    
    globals.trackdb[info_hash].append(val)
    
@app.route("/announce/",methods = ["GET"])
def announce_handler():
    if request.args.get("short") != None and _ENABLE_SHORT_ANNOUNCE == True:
        interval = 120
        interval_min = 30
    
    #mandatory 
    args_info_hash = request.args.get("info_hash")
    args_peer_id = request.args.get("peer_id")
    args_port = request.args.get("port")
    args_uploaded = request.args.get("uploaded")
    args_downloaded = request.args.get("downloaded")
    args_left = request.args.get("left")
    
    #optional
    args_ip = request.args.get("ip")
    if args_ip == None:
        args_ip = request.remote_addr
        
    args_event = request.args.get("event")
    
    
    sum =  args_peer_id.encode("utf-8") + args_info_hash.encode("utf-8")
    
    #When should we remove the client?
    #$expire = time()+$interval;
    expire = 200 #TODO
    
    if sum in globals.db:
        if globals.db[sum]['key'] != request.args.get("key"):
            print "auth failed"
            sleep(3)
            return ""
        
    db_val = {}
    db_val['ip'] = args_ip
    db_val['peer_id'] = args_peer_id
    #db_val['peer_id'] = args_peer_id.encode("utf-8")
    db_val['port'] = args_port
    db_val['expire'] = expire
    db_val['info_hash'] = args_info_hash
    db_val['user_agent'] = request.user_agent.string
    db_val['key'] = request.args.get("key")
    db_val['is_seed'] = is_seed(request)
    
    print db_val
    
    globals.db[sum] = db_val
    
    #add_to_db(args_info_hash,db_val)
    
    if request.args.get("event") == "stopped":
        del globals.db[sum]
        return track([], request)
    
    #cek if any client timeout
    for d in globals.db.iteritems():
        pass
    
    #build reply
    reply_dict = {}
    for k,v in globals.db.iteritems():
        if v['info_hash'] == args_info_hash:
            reply_dict[k] = v
    
    #remove ourself
    del reply_dict[sum]
    
    return track(reply_dict, request)    
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5000)