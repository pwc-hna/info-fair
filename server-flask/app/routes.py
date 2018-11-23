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

@app.route('/')
@app.route('/index')
def index():
    global results
    print("INDEX!")
    return render_template('index.html', title='Home', results=results)


@app.route('/foo', methods=['POST']) 
def foo():
    if not request.json:
        abort(400)
    req_data = request.json
    print req_data
    # Populate our "db"
    new_username = req_data['username']
    new_time = req_data['time']
    new_mistakes = req_data['mistakes']
    results.append({'username':new_username,'time':new_time,'mistakes':new_mistakes})
    return json.dumps(request.json)