# Cloud-Torrent-Control
Torrent Control App allows users to remotely start, stop, and manage torrents through a web interface while their laptop handles the downloading. Built with Flask for the backend and a web interface using HTML, CSS, and JavaScript, it runs over a local network for seamless torrent control.

# Features
Remote Torrent Management – Start, stop, and delete torrents from a web interface.
Real-Time Status Updates – Monitor the download progress and status of active torrents.
Secure Authentication – Access control using user authentication.
Local Network Access – Communicate directly with the torrent client via API.
# Technologies Used
Backend: Flask (Python)
Frontend: HTML, CSS, JavaScript (Flask Jinja templates)
Networking: Local network API communication
Security: HTTP Basic Authentication
# Installation & Setup
Prerequisites
Python 3 installed
uTorrent or BitTorrent installed and running
Flask and required dependencies
1. Clone the Repository
git clone https://github.com/yourusername/Torrent_Control_App.git
cd Torrent_Control_App
2. Install Dependencies
pip install -r requirements.txt
3. Run the Flask Server
python app.py
The server should now be running on http://127.0.0.1:5000 or http://<your-local-ip>:5000.
4. Access the Web Interface
Open your browser and visit:
http://127.0.0.1:5000/dashboard
Manage your torrents remotely.
# Configuration
Ensure uTorrent Web UI is enabled:
Go to Preferences > Advanced > Web UI
Enable Web UI and set a username/password
Update app.py with your uTorrent credentials and IP address if necessary.
# Contributing
Contributions are welcome. Feel free to submit pull requests or open issues for feature requests.







