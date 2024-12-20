from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
import pymysql


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'  # Change this to a secure random key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Admin credentials (store securely in env vars or a database)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = bcrypt.generate_password_hash("mentges99").decode('utf-8')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == ADMIN_USERNAME and bcrypt.check_password_hash(ADMIN_PASSWORD_HASH, data.get('password')):
        session['admin'] = True
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('admin', None)
    return jsonify({"message": "Logged out"}), 200

def is_admin():
    return session.get('admin', False)
