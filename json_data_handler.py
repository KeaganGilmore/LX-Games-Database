import json

DB_FILE = "game_data.json"

# Function to load the existing data from a file
def load_data(filename=DB_FILE):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON from file")
        return {}

# Function to save the updated data to a file
def save_data(data, filename=DB_FILE):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error saving data to file: {e}")

# Function to add new game data for a user
def add_data(user_id, game_type, data):
    game_data = load_data()

    # Extract dob and grade from data
    dob = data.pop("dob", "")
    grade = data.pop("grade", "")

    # Determine the grade key
    if str(grade).isnumeric():
        grade_key = f"grade-{grade}"
    else:
        grade_key = grade

    # Check if the user already exists in the database
    if user_id not in game_data:
        # If not, create a new entry for the user with dob
        game_data[user_id] = {
            "dob": dob
        }
    else:
        # Update dob if it is provided
        if dob:
            game_data[user_id]["dob"] = dob

    # Check if the grade section exists for the user
    if grade_key not in game_data[user_id]:
        # If not, create a new grade section
        game_data[user_id][grade_key] = {}

    # Check if the game type already exists for the user's grade
    if game_type not in game_data[user_id][grade_key]:
        game_data[user_id][grade_key][game_type] = []

    # Append the game data to the user's grade section
    game_data[user_id][grade_key][game_type].append(data)

    # Save the updated data to the file
    save_data(game_data)

# Function to get data for a specific user and game type
def get_data(user_id, game_type):
    game_data = load_data()
    user_data = game_data.get(user_id, {})
    for key in user_data:
        if isinstance(user_data[key], dict) and game_type in user_data[key]:
            return user_data[key][game_type]
    return []

# Function to get all data for a specific user
def get_all_user_data(user_id):
    game_data = load_data()
    return game_data.get(user_id, {})

# Function to get all data for a specific game type across all users
def get_all_data_for_game_type(game_type):
    game_data = load_data()
    result = {}
    for user_id, user_data in game_data.items():
        for key in user_data:
            if isinstance(user_data[key], dict) and game_type in user_data[key]:
                if user_id not in result:
                    result[user_id] = []
                result[user_id].append(user_data[key][game_type])
    return result

def get_all_data_for_grade(grade):
    game_data = load_data()
    result = {}
    grade_key = f"grade-{grade}" if str(grade).isnumeric() else grade
    for user_id, user_data in game_data.items():
        if grade_key in user_data:
            result[user_id] = user_data[grade_key]
    return result