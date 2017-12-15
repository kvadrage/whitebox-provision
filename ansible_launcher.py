#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
###############################################################################
from gevent import monkey
monkey.patch_all()
from gevent import signal
from gevent.wsgi import WSGIServer

import os
import sys
from subprocess import PIPE, Popen
from threading  import Thread
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names

import json
from flask import Flask, jsonify, make_response, abort, request, render_template
from datetime import datetime
import logging


def enqueue_output(out, queue):
    global status
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()
    status = 'FINISHED'


def execute(cmd,path):
  p = Popen(cmd, stdout=PIPE, bufsize=1, close_fds=ON_POSIX, shell=True, cwd=path)
  q = Queue()
  t = Thread(target=enqueue_output, args=(p.stdout, q))
  t.daemon = True # thread dies with the program
  t.start()
  return q
# read line without blocking
# try:  line = q.get_nowait() # or q.get(timeout=.1)
# except Empty:
#     print('no output yet')
# else:
# 	print line

app = Flask(__name__)

status = "READY"
Q = None

def set_logging(filename):
    if filename:
        log_file = logging.FileHandler(os.path.join(os.path.curdir, filename))
        app.logger.addHandler(log_file)
    app.logger.setLevel(logging.INFO)


def loginfo(msg, *args):
    msg = "{}: ".format(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))) + msg.format(*args)
    app.logger.info(msg)


def logerror(msg, *args):
    msg = "{}: ".format(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))) + msg.format(*args)
    app.logger.error(msg)



# route path to full config
@app.route('/api/v1.0/playbooks', methods=['GET'])
def get_playbooks():
    data = []
    loginfo("{} is querrying playbooks", request.remote_addr)
    playbook_files = [ f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.yml')]
    return jsonify({'playbooks': playbook_files })


# route path to get number of switches in db
@app.route('/api/v1.0/status', methods=['GET'])
def get_status():
    loginfo("{} is querrying status", request.remote_addr)
    return jsonify({ 'status': status })

# route path to query a specific playbook
@app.route('/api/v1.0/playbook/<playbook>', methods=['GET'])
def get_playbook(playbook):
    output = None
    loginfo("{} is requesting playbook info: {}", request.remote_addr, playbook)
    if status == 'FINISHED':
        try:  line = Q.get_nowait() # or q.get(timeout=.1)
        except Empty:
            output = 'no output'
        else:
            output = line
    return jsonify({ playbook: {'status': status, 'output': output} })

# route path to run a specific playbook
@app.route('/api/v1.0/playbook/<playbook>/run', methods=['POST'])
def run_playbook(playbook):
    global status, Q
    loginfo("{} is requesting playbook execution: {}", request.remote_addr, playbook)
    if status == 'RUNNING':
        make_response(jsonify({'error':'Already running'}), 400)
    if request.headers['Content-Type'] == 'application/json':
        extra_vars = request.json.get('extra_vars')
        Q = execute('ansible-playbook {}'.format(playbook), os.path.curdir)
        status = 'RUNNING'
        return jsonify({ playbook: status })
    else:
        abort(400)

# handle 400
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error':'Bad request'}), 400)


# handle 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)


# handle 405
@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error':'Method not allowed'}), 405)


# handle 503
@app.errorhandler(503)
def not_available(error):
    return make_response(jsonify({'error':'Service not available'}), 503)


def main():
    set_logging("launcher.log")

    # start server
    loginfo("Starting server...")
    http_server = WSGIServer(('', 8080), app)
    def stop_server():
        loginfo("Stopping server...")
        http_server.close()
    # handle graceful shutdown
    signal(signal.SIGTERM, stop_server)
    signal(signal.SIGINT, stop_server)
    # start serving
    http_server.serve_forever()


if __name__ == "__main__":
    main()
