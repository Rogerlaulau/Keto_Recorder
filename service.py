import sys
import os
import json
 
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file, send_from_directory, safe_join, abort, render_template

from werkzeug.utils import secure_filename
import uuid
from uuid import uuid4

import configparser
config = configparser.ConfigParser()
dir_name = os.path.basename(os.getcwd()).lower()
config.read(f'{dir_name}.conf')
#print(dir_name)
threads = config['service']['threads']
port = config['service'].getint('port')
cleanup_interval = config['service']['cleanup_interval']
channel_timeout = config['service']['channel_timeout']
max_upload_size = config['service']['max_upload_size']
from waitress import serve


from include.Logger import logging, get_logger
log = get_logger(__name__)

app = Flask(__name__)
CORS(app)
 

import DB as db
db.initialize_database()



@app.route("/status", methods=["GET"])
def status():   # for testing connection
    log.info("/status")
    result = {}
    result['status'] = 'OK connected'
    return jsonify(result)


@app.route("/create", methods=["POST"])
def create():
    data = request.json
    log.info(f"/create - data: {data}")
    
    response = db.create_record(data)

    result ={}
    result['status'] = 1
    result['data'] = response
    return jsonify(result)


@app.route("/get_records", methods=["GET"])
def get_records():
    log.info(f"/get_records")
    
    query = db.get_records()
    result ={}
    result['status'] = 1
    result['data'] = query
    return jsonify(result)


@app.route("/home_page", methods=["GET"])
def home():
    log.info(f"/home_page")
    return render_template("home.html")


@app.route("/summary_page", methods=["GET"])
def summary():
    log.info(f"/summary_page")
    return render_template("summary.html")


@app.errorhandler(404)
def error_404(error):
    #log.error(f'error: {error}')
    response = {'status':0, 'message':str(error)}
    return json.dumps(response, indent=4, ensure_ascii=False), 404

@app.errorhandler(Exception)
def error_500(error):
    #log.error(error)
    response = {'status':0, 'message':str(error)}
    return json.dumps(response, indent=4, ensure_ascii=False), 500



if __name__ == '__main__':
    
    log.info(f"Start Service at port: {port}")

    #app.run(host="0.0.0.0", port=port, debug=True)
    serve(app, host='0.0.0.0', port=port, threads=threads, cleanup_interval=cleanup_interval, channel_timeout=channel_timeout)

    