from flask import Flask, request, jsonify
from app.models.blog_model import Post
from app.exceptions.blog_exc import InvalidPostError, FailedDeleteRequest


def init_app(app:Flask):
    @app.get('/posts')
    def read_posts():
        posts = Post.get_all()
        for post in posts:
            del post['_id']
        return jsonify(posts), 200
    
    @app.post('/posts')
    def create_post():
        req = request.get_json()

        try:
            post = Post(**req)
            response = post.save()
            return response, 201
        except (InvalidPostError, TypeError):
            return {'error': 'Invalid entries for creating a new post'}, 400
    
    @app.get('/posts/<int:id>')
    def read_posts_by_id(id):
        post = Post.get_post(id)
        del post['_id']
        return jsonify(post), 200

    @app.delete('/posts/<int:id>')
    def delete_post(id):
        try:
            post = Post.delete(id)
            del post['_id']
            return {'msg': f'Post {post["title"]} deleted'}, 200
        except FailedDeleteRequest:
            return {'error': 'Post could not be deleted'}, 400
        except IndexError:
            return {'error': 'Post does not exist'}, 400


