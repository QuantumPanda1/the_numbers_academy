# backend/community_manager.py
# import pandas as pd
from datetime import datetime
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class CommunityPostManager:
    def __init__(self, storage_type='json'):
        self.storage_type = storage_type
        self.file_path = 'community_posts.json'
        self.initialize_storage()

    def initialize_storage(self):
        """Initialize the storage file if it doesn't exist"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def create_post(self, title, content, category, author):
        """Create a new post"""
        post = {
            'post_id': self._generate_post_id(),
            'title': title,
            'content': content,
            'category': category,
            'author': author,
            'date_posted': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'likes': 0,
            'comments': []
        }

        with open(self.file_path, 'r') as f:
            posts = json.load(f)
        posts.append(post)
        with open(self.file_path, 'w') as f:
            json.dump(posts, f, indent=4)

        return post

    def get_posts(self, category=None, page=1, posts_per_page=10):
        """Retrieve posts with optional filtering and pagination"""
        with open(self.file_path, 'r') as f:
            posts = json.load(f)
        
        if category and category != 'all':
            posts = [post for post in posts if post['category'] == category]
        
        # Sort by date (newest first)
        posts.sort(key=lambda x: x['date_posted'], reverse=True)
        
        # Calculate total pages
        total_posts = len(posts)
        total_pages = (total_posts + posts_per_page - 1) // posts_per_page
        
        # Pagination
        start_idx = (page - 1) * posts_per_page
        end_idx = start_idx + posts_per_page
        
        return {
            'posts': posts[start_idx:end_idx],
            'total_pages': total_pages,
            'current_page': page
        }

    def update_post(self, post_id, updates):
        """Update an existing post"""
        with open(self.file_path, 'r') as f:
            posts = json.load(f)
        
        for post in posts:
            if post['post_id'] == post_id:
                post.update(updates)
                with open(self.file_path, 'w') as f:
                    json.dump(posts, f, indent=4)
                return True
        return False

    def add_comment(self, post_id, comment, author):
        """Add a comment to a post"""
        comment_data = {
            'comment_id': self._generate_comment_id(),
            'content': comment,
            'author': author,
            'date_posted': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open(self.file_path, 'r') as f:
            posts = json.load(f)
        for post in posts:
            if post['post_id'] == post_id:
                post['comments'].append(comment_data)
                with open(self.file_path, 'w') as f:
                    json.dump(posts, f, indent=4)
                return True
        return False

    def _generate_post_id(self):
        """Generate a unique post ID"""
        return datetime.now().strftime('%Y%m%d%H%M%S')

    def _generate_comment_id(self):
        """Generate a unique comment ID"""
        return f"c{datetime.now().strftime('%Y%m%d%H%M%S')}"

# Initialize the post manager
post_manager = CommunityPostManager()

# API Routes
@app.route('/api/posts', methods=['GET'])
def get_posts():
    category = request.args.get('category', 'all')
    page = int(request.args.get('page', 1))
    return jsonify(post_manager.get_posts(category=category, page=page))

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.json
    post = post_manager.create_post(
        title=data['title'],
        content=data['content'],
        category=data['category'],
        author=data.get('author', 'Anonymous')
    )
    return jsonify(post), 201

@app.route('/api/posts/<post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.json
    success = post_manager.add_comment(
        post_id=post_id,
        comment=data['content'],
        author=data.get('author', 'Anonymous')
    )
    return jsonify({'success': success}), 201 if success else 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)