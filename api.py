from flask import Flask, request, jsonify
from json_data_handler import add_data, get_data, get_all_user_data, get_all_data_for_game_type, get_all_data_for_grade
from data_iterator import get_all_users, get_all_games, get_all_grades

app = Flask(__name__)

@app.route('/api/games/<user_id>/<game_type>', methods=['POST'])
def add_game_data_api(user_id, game_type):
    data = request.get_json()
    add_data(user_id, game_type, data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route('/api/games/<user_id>/<game_type>', methods=['GET'])
def get_game_data_api(user_id, game_type):
    # Implementation of getting data for a specific user and game type
    return jsonify({"message": "Get game data for user {} and game type {}".format(user_id, game_type)})

@app.route('/api/games/<user_id>', methods=['GET'])
def get_all_user_game_data_api(user_id):
    # Fetch all game data for the specified user_id
    user_data = get_all_user_data(user_id)  # Assuming get_all_user_data retrieves user data from your data source
    if user_data:
        return jsonify({user_id: user_data})
    else:
        return jsonify({"message": "No game data found for user {}".format(user_id)}), 404


@app.route('/api/games/all/<game_type>', methods=['GET'])
def get_all_game_data_api(game_type):
    # Fetch all game data for the specified game_type
    game_data = get_all_data_for_game_type(game_type)  # Assuming get_all_data_for_game_type retrieves game data from your data source
    if game_data:
        return jsonify({game_type: game_data})
    else:
        return jsonify({"message": "No game data found for game type {}".format(game_type)}), 404


@app.route('/api/users', methods=['GET'])
def get_all_users_api():
    # Implementation of getting a list of all users
    users = get_all_users()
    return jsonify({"users": users})

@app.route('/api/games', methods=['GET'])
def get_all_games_api():
    # Implementation of getting a list of all games
    games = get_all_games()
    return jsonify({"games": games})

@app.route('/api/games/grade/<grade>', methods=['GET'])
def get_all_data_for_grade_api(grade):
    grade_data = get_all_data_for_grade(grade)
    if grade_data:
        return jsonify({grade: grade_data})
    else:
        return jsonify({"message": "No game data found for grade {}".format(grade)}), 404
    
@app.route('/api/grades', methods=['GET'])
def get_grades_api():
    grades = get_all_grades()
    return jsonify({"grades": grades})
    


if __name__ == "__main__":
    app.run(debug=True)
