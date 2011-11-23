import hashlib

from flask import Flask
from flask import render_template
from flask import request
from werkzeug.wrappers import Request
from flask import g
from flask import globals

app = Flask(__name__)

globals.db = {}
globals.TRACKER = {}
globals.TRACKER['open_tracker'] = True
globals.TRACKER['announce_interval'] = 1800
globals.TRACKER['min_interval'] = 900
globals.TRACKER['default_peers'] = 50
globals.TRACKER['max_peers'] = 100

globals.TRACKER['external_ip'] = True
globals.TRACKER['force_compact'] = False
globals.TRACKER['full_scrape'] = False
globals.TRACKER['random_limits'] = 500
globals.TRACKER['clean_idle_peers'] = 10


@app.route("/announce",methods = ["GET"])
def announce_handler():
    c_tracker = globals.TRACKER
    
    arg_info_hash = request.args.get("info_hash")
    arg_peer_id = request.args.get("peer_id")
    arg_port = request.args.get("port")
    arg_left = request.args.get("left")
    
    #2o bytes info_hash
    if arg_info_hash == None or len(arg_info_hash) != 20:
        return
    
    #20 bytes peer_id
    if arg_peer_id == None or len(arg_peer_id) != 20:
        return
    
    if left != None:
        if left > 0:
            c_tracker['seeding'] = 0
        else:
            c_tracker['seeding'] = 1
    
    arg_compact = request.args.get("compact")
    if arg_compact == None and c_tracker['force_compact'] == True:
        arg_compact = 1
    else:
        arg_compact = int(arg_compact)
    
    arg_no_peer_id = request.args.get("no_peer_id")
    if arg_no_peer_id == None:
        arg_no_peer_id = 0
    else:
        arg_no_peer_id = int(arg_no_peer_id)
    
    arg_ip = request.args.get("ip")
    if arg_ip != None and c_tracker['external_ip'] == True:
        arg_ip = request.args.get("ip")
    else:
        arg_ip = request.remote_addr
        
    arg_numwant = request.args.get("numwant")
    if arg_numwant == None:
        arg_numwant = c_tracker["default_peers"]
    elif int(arg_numwant) > c_tracker["max_peers"]:
        arg_numwant = c_tracker["max_peers"]
    else:
        arg_numwant = int(arg_numwant)
        
    
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)