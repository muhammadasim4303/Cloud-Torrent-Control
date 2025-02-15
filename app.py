from flask import Flask, render_template, jsonify, request
import requests
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
auth = HTTPBasicAuth()

utorrent_url = "http://127.0.0.1:8000/gui/"

print("Enter your username: ")
VALID_USERNAME = str(input())
print("Enter your password: ")
VALID_PASSWORD = str(input())

def fetch_token():
    session = requests.Session()
    session.auth = (VALID_USERNAME, VALID_PASSWORD)
    session.headers.update({"Referer": utorrent_url})

    token_url = f"{utorrent_url}token.html"
    response = session.get(token_url)

    if response.status_code == 200:
        token_start = response.text.find("'>") + 2
        token_end = response.text.find("</div>")
        return response.text[token_start:token_end]
    return None

@auth.verify_password
def verify_password(username, password):
    return username == VALID_USERNAME and password == VALID_PASSWORD

def fetch_torrents(username, password):
    session = requests.Session()
    session.auth = (username, password)
    session.headers.update({"Referer": utorrent_url})

    token_url = f"{utorrent_url}token.html"
    response = session.get(token_url)

    if response.status_code == 200:
        token_start = response.text.find("'>") + 2
        token_end = response.text.find("</div>")
        token = response.text[token_start:token_end]

        list_url = f"{utorrent_url}?list=1&token={token}"
        list_response = session.get(list_url)

        if list_response.status_code == 200:
            try:
                return list_response.json().get("torrents", [])
            except ValueError:
                return []
    return []

@app.route('/api/torrent-control', methods=['POST'])
def control_torrent():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Missing JSON payload"}), 400

    hash_value = data.get('hash')
    action = data.get('action')

    if not hash_value or not action:
        return jsonify({"success": False, "error": "Missing hash or action parameter"}), 400


    session = requests.Session()
    session.auth = (VALID_USERNAME, VALID_PASSWORD)
    session.headers.update({"Referer": utorrent_url})

    token_url = f"{utorrent_url}token.html"
    response = session.get(token_url)

    if response.status_code == 200:
        token_start = response.text.find("'>") + 2
        token_end = response.text.find("</div>")
        token = response.text[token_start:token_end]

        if action == 'start':
            action_url = f"{utorrent_url}?action=start&hash={hash_value}&token={token}"
        elif action == 'stop':
            action_url = f"{utorrent_url}?action=stop&hash={hash_value}&token={token}"
        elif action == 'delete':
            action_url = f"{utorrent_url}?action=remove&hash={hash_value}&token={token}"
        else:
            return jsonify({"success": False, "error": "Invalid action"}), 400

        action_response = session.get(action_url)

        if action_response.status_code == 200:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Failed to perform action"}), action_response.status_code

    return jsonify({"success": False, "error": "Failed to fetch token"}), 500

@app.route('/dashboard')
def dashboard():
    return render_template('torrents.html')

@app.route('/api/torrents')
def get_torrents():
    torrents = fetch_torrents(VALID_USERNAME, VALID_PASSWORD)
    if not torrents:
        return jsonify({"error": "No torrents available or failed to fetch."}), 500
    return jsonify(torrents)

@app.route('/api/authenticate', methods=['POST'])
def authenticate_user():
    if not request.is_json:
        return jsonify({"message": "Invalid content type. Must be JSON."}), 400
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return jsonify({"message": "Authentication successful"}), 200
    return jsonify({"message": "Authentication failed"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
