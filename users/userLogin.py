import json
import requests
import jwt

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
        # Decode the token without verifying the signature
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
    except jwt.exceptions.DecodeError:
        print("Error: Invalid token")
        return None

# Example usage:
if __name__ == "__main__":
    input_json = '''{
        "Username": {
            "cursor": 14,
            "candidate_text": {
                "length": 0,
                "text": "",
                "start": 0
            },
            "text": "KeaganGilmore",
            "text_draw_offset": 0
        },
        "Password": {
            "cursor": 10,
            "candidate_text": {
                "length": 0,
                "text": "",
                "start": 0
            },
            "text": "keagan004",
            "text_draw_offset": 0
        }
    }'''

    parsed_data = parse_json_login(input_json)
    if parsed_data:
        api_response, status_code = post_to_external_api(parsed_data)
        if status_code == 200:
            token = api_response.decode('utf-8')
            decoded_token = decode_jwt_token(token)
            if decoded_token:
                print("Decoded Token:", decoded_token)
            else:
                print("Failed to decode token")
        else:
            print(api_response, status_code)
