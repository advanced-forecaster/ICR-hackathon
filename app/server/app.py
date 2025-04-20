from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import json
import glob

app = Flask(__name__)
CORS(app)

CALENDAR_DIR = "calendar_data"

os.makedirs(CALENDAR_DIR, exist_ok=True)

def get_day_file_path(date_str):
    return os.path.join(CALENDAR_DIR, f"{date_str}.txt")

@app.route('/tasks/month/<year>/<month>', methods=['GET'])
def get_month_tasks(year, month):
    try:
        datetime.strptime(f"{year}-{month}", '%Y-%m')
        pattern = os.path.join(CALENDAR_DIR, f"{year}-{month}-*.txt")
        files = glob.glob(pattern)
        tasks = {}
        for file_path in files:
            date = os.path.basename(file_path).replace('.txt', '')
            with open(file_path, 'r') as f:
                tasks[date] = f.read()
        return jsonify(tasks), 200
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<date>', methods=['GET'])
def get_task(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        file_path = get_day_file_path(date)
        if not os.path.exists(file_path):
            return jsonify({'task': ''}), 200
        with open(file_path, 'r') as f:
            task = f.read()
        return jsonify({'task': task}), 200
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<date>', methods=['POST'])
def add_tasks(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        data = request.get_json()
        if not data or 'task' not in data:
            return jsonify({'error': 'Task is required'}), 400
        file_path = get_day_file_path(date)
        with open(file_path, 'w') as f:
            f.write(data['task'])
        return jsonify({'message': 'Task added successfully'}), 201
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<date>', methods=['PUT'])
def edit_tasks(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        data = request.get_json()
        if not data or 'task' not in data:
            return jsonify({'error': 'Task is required'}), 400
        file_path = get_day_file_path(date)
        if not os.path.exists(file_path):
            return jsonify({'error': 'No task found for this date'}), 404
        with open(file_path, 'w') as f:
            f.write(data['task'])
        return jsonify({'message': 'Task updated successfully'}), 200
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        return jsonify({
            'role': 'assistant',
            'text': data['message']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
