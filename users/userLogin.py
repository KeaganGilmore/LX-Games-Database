import json
import requests
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

# Get the necessary credentials from environment variables
login_url = os.getenv('LOGIN_URL')
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

def parse_json_login(json_str):
    try:
        data = json.loads(json_str)
        email = data.get("Username", {}).get("text", "")
        password = data.get("Password", {}).get("text", "")
        return {"email": email, "password": password}
    except json.JSONDecodeError:
        print("Invalid JSON input.")
        return None

def post_to_external_api(parsed_data):
    try:
        response = requests.post("https://lxlibrary.online/api/login/student", json=parsed_data)
        if response.status_code == 200:
            return response.content, response.status_code
        else:
            return {"error": "Failed to post data to external API", "status_code": response.status_code}, response.status_code
    except Exception as e:
        print("Error:", e)
        return {"error": "Failed to post data to external API"}, 500

def decode_jwt_token(token):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
    except jwt.exceptions.DecodeError:
        print("Error: Invalid token")
        return None

def get_bearer_token(login_url, email, password):
    payload = {
        'email': email,
        'password': password
    }
    response = requests.post(login_url, json=payload)
    if response.status_code == 200:
        return response.text.strip()
    else:
        print(f'Failed to log in. Status code: {response.status_code}')
        print("Response content:", response.text)
        raise Exception('Failed to log in.')

def summarize_course_details(course_details):
    summarized_courses = {}
    for course in course_details:
        summarized_course = {
            "id": course.get("id"),
            "name": course.get("name"),
            "lessons": []
        }
        for lesson in course.get("Lessons", []):
            summarized_lesson = {
                "id": lesson.get("id"),
                "title": lesson.get("title"),
                "image_slides": []
            }
            for slide in lesson.get("Slides", []):
                if slide.get("type") == "IMAGE":
                    summarized_lesson["image_slides"].append({
                        "id": slide.get("id"),
                        "title": slide.get("title")
                    })
            summarized_course["lessons"].append(summarized_lesson)
        summarized_courses[course.get("id")] = summarized_course
    return summarized_courses

def fetch_and_save_course_details(bearer_token, course_ids, student_data, output_file):
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }
    course_details = []

    # Load existing data from the file if it exists
    existing_data = {}
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            existing_data = json.load(file)

    for course_id in course_ids:
        url = f'https://lxlibrary.online/api/course/{course_id}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            course_details.append(response.json())
        else:
            print(f'Failed to get details for course ID {course_id}. Status code: {response.status_code}')
    
    summarized_courses = summarize_course_details(course_details)
    student_id = student_data['id']

    # Update or add the student data to the existing file
    if student_id in existing_data:
        existing_data[student_id]['courses'] = summarized_courses
    else:
        existing_data[student_id] = student_data
        existing_data[student_id]['courses'] = summarized_courses

    with open(output_file, 'w') as file:
        json.dump(existing_data, file, indent=4)
    print(f'Successfully saved summarized course details to {output_file}')


def main(input_json):
    parsed_data = parse_json_login(input_json)
    if parsed_data:
        api_response, status_code = post_to_external_api(parsed_data)
        if status_code == 200:
            token = api_response.decode('utf-8')
            decoded_token = decode_jwt_token(token)
            if decoded_token:
                try:
                    bearer_token = get_bearer_token(login_url, email, password)
                    course_ids = decoded_token.get('courses', [])
                    if course_ids:
                        student_data = decoded_token.copy()
                        fetch_and_save_course_details(bearer_token, course_ids, student_data, 'game_users.json')
                        # Return only the student data that was just added or updated
                        student_id = student_data['id']
                        with open('game_users.json', 'r') as file:
                            json_data = json.load(file)
                            return json_data.get(student_id, {})
                    else:
                        return {"error": "No course IDs found for the student."}
                except Exception as e:
                    return {"error": f'Error: {e}'}
            else:
                return {"error": "Failed to decode token"}
        else:
            return {"error": api_response, "status_code": status_code}
    else:
        return {"error": "Invalid input JSON."}