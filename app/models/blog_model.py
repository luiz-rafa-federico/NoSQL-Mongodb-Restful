from . import db
from datetime import datetime
from app.exceptions.blog_exc import InvalidPostError, FailedDeleteRequest, EmptyPostsError

class Post():
    def __init__(self, title, author, tags, content):
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content
        self.created_at = datetime.utcnow().strftime('%d/%m/%Y %I:%M%p').lower()
        self.updated_at = self.created_at
        self.id = 0


    @staticmethod
    def validate(title, author, tags, content):
        if not type(title) == str or not len(title) or not type(author) == str or not len(author) or not type(content) == str or not len(content) or not type(tags) == list or not len(tags):
                raise TypeError
        
    
    @staticmethod
    def validate_to_update(request):
        if request.get('title'): 
            if not type(request.get('title')) == str or not len(request.get('title')):
                raise TypeError
        if request.get('author'):
            if not type(request.get('author')) == str or request.get('author') == " ":
                raise TypeError
        if request.get('content'):
            if not type(request.get('content')) == str or request.get('content') == " ":
                raise TypeError
        if request.get('tags'):
            if not type(request.get('tags')) == list or len(request.get('tags')) == 0:
                raise TypeError
    

    @staticmethod
    def get_all():
        posts = list(db.posts.find())

        if not posts:
            raise EmptyPostsError
        return posts
    

    @staticmethod
    def get_post(id):
        searched_post = db.posts.find_one({"id": id})

        if not searched_post:
            raise IndexError

        return searched_post


    def save(self):
        posts = list(db.posts.find())

        self.id = 1 if not posts else posts[-1]['id'] + 1

        req_post = {'title': self.title, 'author': self.author, 'id': self.id, "content": self.content, 'created_at': self.created_at, 'tags': self.tags, 'updated_at': self.updated_at}

        _id = db.posts.insert_one(req_post).inserted_id

        if not _id:
            raise InvalidPostError

        new_post = db.posts.find_one({'_id': _id})

        del new_post['_id']
        return new_post


    @staticmethod
    def update(id, title=None, author=None, tags=None, content=None):
        to_be_updated = db.posts.find_one({'id': id})
        time_updated = datetime.utcnow().strftime('%d/%m/%Y %I:%M%p').lower()

        if not to_be_updated:
            raise IndexError
        else:
            if title:
                new_title = {"$set": {"title": title, "updated_at": time_updated}}
                db.posts.update_one(to_be_updated, new_title)
            elif author:
                new_author = {"$set": {"author": author, "updated_at": time_updated}}
                db.posts.update_one(to_be_updated, new_author)
            elif content:
                new_content = {"$set": {"content": content, "updated_at": time_updated}}
                db.posts.update_one(to_be_updated, new_content)
            elif tags:
                new_tags = {"$set": {"tags": tags, "updated_at": time_updated}}
                db.posts.update_one(to_be_updated, new_tags)

        updated_post = db.posts.find_one({'id': id})

        return updated_post

    
    @staticmethod
    def delete(id):
        posts = list(db.posts.find())
        deleted_post = [post for post in posts if post['id'] == int(id)][0]
        db.posts.delete_one({"id": deleted_post['id']})
        
        if not deleted_post:
            if IndexError:
                raise IndexError
            raise FailedDeleteRequest

        return deleted_post
        


