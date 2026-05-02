
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
PORT = 8000

TEST_API_BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJnczIxNDRAc3JtaXN0LmVkdS5pbiIsImV4cCI6MTc3NzcwMjIxMSwiaWF0IjoxNzc3NzAxMzExLCJpc3MiOiJBZmZvcmQgTWVkaWNhbCBUZWNobm9sb2dpZXMgUHJpdmF0ZSBMaW1pdGVkIiwianRpIjoiMWU1N2VhNDYtYjk5NC00NDhjLWI2ZGQtM2EyMjhjNjQ3NzA1IiwibG9jYWxlIjoiZW4tSU4iLCJuYW1lIjoiZ3VyYmFrc2ggc2luZ2giLCJzdWIiOiIxMjU0M2VhNC05NTM4LTRlMmUtOGEzNS1lZTdhNmUxMjc2NDgifSwiZW1haWwiOiJnczIxNDRAc3JtaXN0LmVkdS5pbiIsIm5hbWUiOiJndXJiYWtzaCBzaW5naCIsInJvbGxObyI6InJhMjMxMTAwMzAzMDEwNiIsImFjY2Vzc0NvZGUiOiJRa2JweEgiLCJjbGllbnRJRCI6IjEyNTQzZWE0LTk1MzgtNGUyZS04YTM1LWVlN2E2ZTEyNzY0OCIsImNsaWVudFNlY3JldCI6IlFkSnp1QVpjUGh4cURQRUIifQ.aZCNuwJEO8inWyGWb9fUImSRc2UenfFKUolcJ-oAQW8"

stacks = ['backend', 'frontend']
levels = ['debug', 'info', 'warn', 'error', 'fatal']
packages = [
    'cache', 'controller', 'cron_job', 'db', 'domain', 'handler',
    'repository', 'route', 'service', 'api', 'component', 'hook',
    'page', 'state', 'style', 'auth', 'config', 'middleware', 'utils'
]

def Log(stack, level, packageName, message):
    if stack not in stacks:
        return {"error": "Invalid stack"}, 400
    if level not in levels:
        return {"error": "Invalid level"}, 400
    if packageName not in packages:
        return {"error": "Invalid package"}, 400
    if not message:
        return {"error": "No message provided"}, 400

    url = "http://20.207.122.201/evaluation-service/logs"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TEST_API_BEARER_TOKEN}"
    }

    payload = {
        "stack": stack,
        "level": level,
        "package": packageName,
        "message": message
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if 200 <= response.status_code < 300:
            return response.json(), 200
        else:
            return response.json(), response.status_code

    except Exception as e:
        return {"error": str(e)}, 500



def require_token():
    auth_header = request.headers.get("Authorization ", "")
    
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401

    token = auth_header[7:]
    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    return None


@app.route("/", methods=["GET"])
def home():
    return "Test ..."


@app.route("/log", methods=["POST"])
def log_route():
    auth_error = require_token()
    if auth_error:
        return auth_error

    data = request.get_json()

    stack = data.get("stack")
    level = data.get("level")
    packageName = data.get("package")
    message = data.get("message")

    result, status_code = Log(stack, level, packageName, message)

    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
