# json_data_handler.py

import json

DB_FILE = "game_data.json"

def load_data():
    try:
        with open(DB_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_data(game_type, data):
    game_data = load_data()
    if game_type not in game_data:
        game_data[game_type] = []
    game_data[game_type].append(data)
    save_data(game_data)

def get_data(game_type):
    game_data = load_data()
    return game_data.get(game_type, [])