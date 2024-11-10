import csv
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CSV_FILE = 'comments.csv'

def initialize_csv():
    try:
        with open(CSV_FILE, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'email', 'comment', 'timestamp'])
    except FileExistsError:
        pass  # File already exists, no need to initialize

def add_comment(name, email, comment):
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, comment, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

def get_comments():
    comments = []
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            comments.append({
                'name': row['name'],
                'comment': row['comment'],
                'timestamp': row['timestamp']
            })
    return comments[::-1]  # Return comments in reverse order (newest first)

@app.route('/api/comments', methods=['POST'])
def post_comment():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    comment = data.get('comment')
    
    if not all([name, email, comment]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    add_comment(name, email, comment)
    return jsonify({'message': 'Comment added successfully'}), 201

@app.route('/api/comments', methods=['GET'])
def fetch_comments():
    comments = get_comments()
    return jsonify(comments)

if __name__ == '__main__':
    initialize_csv()
    app.run(debug=True)