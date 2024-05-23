import json

def get_all_users():
    with open('game_data.json') as f:
        data = json.load(f)
    return list(data.keys())

def get_all_games():
    with open('game_data.json') as file:
        data = json.load(file)
        games = set()
        for user, user_data in data.items():
            for grade, grade_data in user_data.items():
                if grade != 'dob':
                    for game_type, game_data in grade_data.items():
                        games.add(game_type)
        return list(games)

def get_all_grades():
    grades = set()
    with open('game_data.json') as f:
        data = json.load(f)

    for user_data in data.values():
        for key in user_data:
            if key.startswith('grade-') or key == 'undergraduate' or key == 'graduate' or key == 'preschool':
                grades.add(key)

    return list(grades)