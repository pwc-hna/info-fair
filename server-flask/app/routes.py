from app import app
from flask import render_template, abort, request
import json

results = [
        {
            'username':'Horia',
            'time':'00:12:99',
            'mistakes':'1'
        },
        {
            'username':'Robocop',
            'time':'00:05:77',
            'mistakes':'0'
        }
        ]

live_players = [
    {
        'username' : 'sample_destroyer',
        'current_doc' : '0',
        'total_docs' : '20'
    }
]

@app.route('/')
@app.route('/index')
def index():
    global results
    return render_template('index.html', title='Home', results=results,live_players=live_players)


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
                'username':incoming_username,
                'time':incoming_time,
                'mistakes':incoming_mistakes
                }
    except KeyError:
        print "ERROR invalid JSON data " + req_data
        return

    # Populate our "db"
    results.append(incoming_finishing_player)
    for live_player in live_players:
        if live_player['username'] == incoming_username:
            live_players.remove(live_player)
            break
    return json.dumps(request.json)


@app.route('/progress', methods=['POST']) 
def progress():
    if not request.json:
        print "ERROR no json"
        abort(400)
    req_data = request.json

    # Validate input data
    try:
        incoming_username = req_data['username']
        incoming_current_document = req_data['current_doc']
        incoming_total_documents = req_data['total_docs']
        incoming_live_player = {
                'username':incoming_username,
                'current_doc':incoming_current_document,
                'total_docs':incoming_total_documents
                }
    except KeyError:
        print "ERROR invalid JSON data " + req_data
        return

    found = False
    for live_player in live_players:
        if live_player['username'] == incoming_username:
            found = True
            # Replace the whole user entry
            live_players[live_players.index(live_player)] = incoming_live_player
            break
    if not found:
        live_players.append(incoming_live_player)
    return json.dumps(request.json)