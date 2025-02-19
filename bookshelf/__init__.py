from flask import Flask
from .model import Base

def create_application() -> Flask:
    application = Flask(__name__)
    return application
