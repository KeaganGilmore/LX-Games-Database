import json
import requests
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

def get_course_ids_from_student(student):
    course_ids = []
    for key, value in student.items():
        if isinstance(value, dict) and "slider" in value:
            for session in value["slider"]:
                course_ids.append(session["id"])
    return course_ids

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

def fetch_and_save_course_details(bearer_token, course_ids):
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }
    course_details = []
    
    for course_id in course_ids:
        url = f'https://lxlibrary.online/api/course/{course_id}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            course_details.append(response.json())
        else:
            print(f'Failed to get details for course ID {course_id}. Status code: {response.status_code}')
    
    summarized_courses = summarize_course_details(course_details)
    return summarized_courses

def main():
    try:
        bearer_token = get_bearer_token(login_url, email, password)
        
        with open('game_users.json', 'r') as file:
            students_data = json.load(file)
        
        for student_id, student in students_data.items():
            course_ids = get_course_ids_from_student(student)
            if course_ids:
                summarized_courses = fetch_and_save_course_details(bearer_token, course_ids)
                students_data[student_id]["courses"] = summarized_courses
            else:
                print(f"No course IDs found for the student {student_id}.")
        
        with open('game_users_with_courses.json', 'w') as file:
            json.dump(students_data, file, indent=4)
        
        print(f"Successfully saved detailed course data to 'game_users_with_courses.json'")

    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
