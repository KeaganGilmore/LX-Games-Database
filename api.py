from flask import Flask, request, jsonify
from json_data_handler import add_data, get_data, get_all_user_data, get_all_data_for_game_type

app = Flask(__name__)

@app.route('/api/games/<user_id>/<game_type>', methods=['POST'])
def add_game_data_api(user_id, game_type):
    data = request.json
    add_data(user_id, game_type, data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route('/api/games/<user_id>/<game_type>', methods=['GET'])
def get_game_data_api(user_id, game_type):
    return jsonify(get_data(user_id, game_type))

@app.route('/api/games/<user_id>', methods=['GET'])
def get_all_user_game_data_api(user_id):
    return jsonify(get_all_user_data(user_id))

@app.route('/api/games/all/<game_type>', methods=['GET'])
def get_all_game_data_api(game_type):
    return jsonify(get_all_data_for_game_type(game_type))

if __name__ == "__main__":
    app.run(debug=True)
