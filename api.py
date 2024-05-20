# api.py

from flask import Flask, request, jsonify
from json_data_handler import add_data, get_data

app = Flask(__name__)

@app.route('/api/games/<game_type>', methods=['POST'])
def add_game_data_api(game_type):
    data = request.json
    add_data(game_type, data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route('/api/games/<game_type>', methods=['GET'])
def get_game_data_api(game_type):
    return jsonify(get_data(game_type))

if __name__ == "__main__":
    app.run(debug=True)
