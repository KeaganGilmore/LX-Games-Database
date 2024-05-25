import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the necessary credentials from environment variables
login_url = os.getenv('LOGIN_URL')
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

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

def get_course_ids_from_file(file_path, student_id):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            student = next((s for s in data if s['id'] == student_id), None)
            if student:
                return [course['id'] for course in student['Courses']]
            else:
                print("Student not found.")
                return []
    except FileNotFoundError:
        print("File not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return []

def summarize_course_details(course_details):
    summarized_courses = []
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
        summarized_courses.append(summarized_course)
    return summarized_courses

def fetch_and_save_course_details(bearer_token, course_ids, output_file):
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }
    course_details = []

    for course_id in course_ids:
        url = f'https://lxlibrary.online/course/{course_id}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            course_details.append(response.json())
        else:
            print(f'Failed to get details for course ID {course_id}. Status code: {response.status_code}')
    
    summarized_courses = summarize_course_details(course_details)

    with open(output_file, 'w') as file:
        json.dump(summarized_courses, file, indent=4)
    print(f'Successfully saved summarized course details to {output_file}')

def main(student_id):
    try:
        bearer_token = get_bearer_token(login_url, email, password)
        course_ids = get_course_ids_from_file('users.json', student_id)
        if course_ids:
            fetch_and_save_course_details(bearer_token, course_ids, 'courses.json')
        else:
            print("No course IDs found for the student.")
    except Exception as e:
        print(f'Error: {e}')

