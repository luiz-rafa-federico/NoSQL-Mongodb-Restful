from flask import Flask, request, jsonify
from app.models.blog_model import Post
from app.exceptions.blog_exc import InvalidPostError, FailedDeleteRequest, EmptyPostsError
from http import HTTPStatus


def init_app(app:Flask):
    @app.get('/posts')
    def read_posts():
        try:
            posts = Post.get_all()
            for post in posts:
                del post['_id']
            return jsonify(posts), HTTPStatus.OK
        except EmptyPostsError:
            return {'error': 'No posts created yet'}, HTTPStatus.NOT_FOUND
    

    @app.post('/posts')
    def create_post():
        req = request.get_json()
        try:
            Post.validate(**req)
            post = Post(**req)
            response = post.save()
            return response, HTTPStatus.CREATED
        except (InvalidPostError, TypeError):
            return {'error': 'Invalid entries for creating a post'}, HTTPStatus.BAD_REQUEST
    

    @app.get('/posts/<int:id>')
    def read_posts_by_id(id):
        try:
            post = Post.get_post(id)
            del post['_id']
            return jsonify(post), HTTPStatus.OK
        except IndexError:
            return {'error': 'Post does not exist'}, HTTPStatus.NOT_FOUND
    

    @app.route('/posts/<int:id>', methods=['PATCH'])
    def update_post(id):
        data = request.get_json()
        try:
            Post.validate_to_update(data)
            post = Post.update(id, **data)
            del post['_id']
            return {'msg': f'Post updated successfully'}, HTTPStatus.OK
        except IndexError:
            return {'error': 'Post does not exist'}, HTTPStatus.NOT_FOUND
        except TypeError:
            return {'error': 'Invalid entries for updating a post'}, HTTPStatus.BAD_REQUEST


    @app.delete('/posts/<int:id>')
    def delete_post(id):
        try:
            post = Post.delete(id)
            del post['_id']
            return {'msg': f'Post {post["title"]} deleted successfully'}, HTTPStatus.OK
        except FailedDeleteRequest:
            return {'error': 'Post could not be deleted'}, HTTPStatus.BAD_REQUEST
        except IndexError:
            return {'error': 'Post does not exist'}, HTTPStatus.NOT_FOUND