from app import app
from flask import render_template, abort, request
import json
from db import *

db.create_all()

results = []

live_players = []


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Leaderboards', results_humans=db_get_all_finished_humans_as_list(), results_robots= db_get_all_finished_robots_as_list(),live_players=db_get_all_live_users_as_list())

@app.route('/index_refresh')
def index_refresh():
    return render_template('index_refresh.html', title='Leaderboards', results_humans=db_get_all_finished_humans_as_list(), results_robots= db_get_all_finished_robots_as_list(),live_players=db_get_all_live_users_as_list())

@app.route('/finished', methods=['POST'])
def finished():
    if not request.json:
        abort(400)
    req_data = request.json

    # Validate input data
    try:
        incoming_username = req_data['username']
        incoming_time = req_data['time']
        incoming_mistakes = req_data['mistakes']
        incoming_finishing_player = {
            'username': incoming_username,
            'time': incoming_time,
            'mistakes': incoming_mistakes
        }
    except KeyError:
        print "ERROR invalid JSON data " + req_data
        return

    db_add_finishing_player(incoming_finishing_player)
    return json.dumps(request.json)


@app.route('/progress', methods=['POST'])
def progress():
    if not request.json:
        print "ERROR no json"
        abort(400)
    req_data = request.json

    try:
        incoming_username = req_data['username']
        incoming_current_document = req_data['current_doc']
        incoming_total_documents = req_data['total_docs']
        incoming_live_player = {
            'username': incoming_username,
            'current_doc': incoming_current_document,
            'total_docs': incoming_total_documents
        }
    except KeyError:
        print "ERROR invalid JSON data " + req_data
        return

    db_user_update_live_player(incoming_live_player)

    return json.dumps(request.json)

@app.route('/quit', methods=['POST'])
def quit():
    if not request.json:
        print "ERROR no json"
        abort(400)
    req_data = request.json

    try:
        incoming_username = req_data['username']
    except KeyError:
        print "ERROR invalid JSON data " + req_data
        return

    if db_user_is_live(incoming_username):
        db_rm_live_player(incoming_username)
    return json.dumps(request.json)
