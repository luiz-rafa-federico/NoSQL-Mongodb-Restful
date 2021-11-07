from . import db
from datetime import datetime
from app.exceptions.blog_exc import InvalidPostError, FailedDeleteRequest

class Post():
    def __init__(self, title, author, tags, content):
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content
        self.created_at = datetime.now().strftime('%d/%m/%Y %I:%M%p').lower()
        self.updated_at = datetime.now().strftime('%d/%m/%Y %I:%M%p').lower()
        self.id = 0
    

    @staticmethod
    def get_all():
        posts = list(db.posts.find())
        return posts
    

    @staticmethod
    def get_post(id):
        posts = list(db.posts.find())
        searched_post = [post for post in posts if post['id'] == int(id)][0]
        return searched_post


    def save(self):
        posts = list(db.posts.find())

        self.id = 1 if not posts else posts[-1]['id'] + 1

        req_post = {'title': self.title, 'author': self.author, 'id': self.id, "content": self.content, 'created_at': self.created_at, 'tags': self.tags}

        _id = db.posts.insert_one(req_post).inserted_id

        if not _id:
            raise InvalidPostError

        new_post = db.posts.find_one({'_id': _id})

        del new_post['_id']
        return new_post
    

    @staticmethod
    def delete(id):
        posts = list(db.posts.find())
        deleted_post = [post for post in posts if post['id'] == int(id)][0]
        db.posts.delete_one({"id": deleted_post['id']})
        
        if not deleted_post:
            raise IndexError

        return deleted_post
        


