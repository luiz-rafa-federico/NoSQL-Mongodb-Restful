from flask import Flask
from app.controllers import blog_controller

def create_app():
    app = Flask(__name__)
    blog_controller.init_app(app)
    return app
