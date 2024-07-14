from flask import Flask, request, jsonify, render_template, redirect
import json
from datetime import datetime
import threading
import time
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# Retrieve the bot token from the environment variable
Invite = os.getenv('DISCORD_INVITE')

# Function to load JSON data from file
def load_data():
    with open('users.json') as f:
        return json.load(f)

# Load JSON data initially
data = load_data()

# Function to format ISO datetime to a more readable format
def format_datetime(iso_datetime):
    if iso_datetime:
        dt = datetime.fromisoformat(iso_datetime)
        return dt.strftime('%Y-%m-%d %H:%M:%S')  # Customize the format as desired
    else:
        return ''

# Function to get top 10 users by XP
def get_top_10_by_xp():
    sorted_data = sorted(data.items(), key=lambda x: x[1]['xp'], reverse=True)
    top_10 = sorted_data[:10]
    return [{'id': key, **value} for key, value in top_10]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    
    if not query:
        return jsonify({'error': 'Invalid search query'}), 400
    
    results = []
    
    # Check if the query is a number (ID) or string (Name)
    if query.isdigit():  # If the query is numeric, assume it's an ID
        if query in data:
            results.append({query: data[query]})
    else:  # Otherwise, assume it's a name
        for key, value in data.items():
            if query.lower() in value.get('name', '').lower():
                results.append({key: value})
    
    # Format dates before passing to template
    for result in results:
        for key, value in result.items():
            value['first_login'] = format_datetime(value.get('first_login'))
            value['last_login'] = format_datetime(value.get('last_login'))
    
    return jsonify(results)

@app.route('/top10xp', methods=['GET'])
def top_10_by_xp():
    top_10 = get_top_10_by_xp()
    return jsonify(top_10)

@app.route('/invite')
def invite():
    return redirect(Invite)

def update_data_periodically():
    global data
    while True:
        data = load_data()
        time.sleep(60)  # Update data every minute

if __name__ == '__main__':
    threading.Thread(target=update_data_periodically).start()
    app.run(debug=True)
