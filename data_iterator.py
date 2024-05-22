import json

def get_all_users():
    with open('game_data.json') as f:
        data = json.load(f)
    return list(data.keys())

def get_all_games():
    with open('game_data.json') as file:
        data = json.load(file)
    
    games = []
    for user, user_data in data.items():
        for game in user_data:
            games.append(game)
    
    return games