import json

DB_FILE = "game_data.json"

def load_data():
    try:
        with open(DB_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    except json.JSONDecodeError:
        data = {}
    return data

def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_data(user_id, game_type, data):
    game_data = load_data()
    if user_id not in game_data:
        game_data[user_id] = {}
    if game_type not in game_data[user_id]:
        game_data[user_id][game_type] = []
    game_data[user_id][game_type].append(data)
    save_data(game_data)

def get_data(user_id, game_type):
    game_data = load_data()
    return game_data.get(user_id, {}).get(game_type, [])

def get_all_user_data(user_id):
    game_data = load_data()
    return game_data.get(user_id, {})

def get_all_data_for_game_type(game_type):
    game_data = load_data()
    result = {}
    for user_id, user_data in game_data.items():
        if game_type in user_data:
            result[user_id] = user_data[game_type]
    return result
