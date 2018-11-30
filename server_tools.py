import json
import requests
import settings

def post_json_to_server(json, route):
    requests.post(settings.serverAddress + route, json=json)

def post_game_end_json(player_name, final_time, mistakes):
    post_json_to_server(json={"username": player_name, "time":final_time,"mistakes":mistakes},route='/finished')

def post_player_progress_json(player_name, current_doc, total_docs):
    post_json_to_server(json={"username": player_name, "current_doc":current_doc,"total_docs":total_docs},route='/progress')
