"""Flask configuration variables"""
from dotenv import load_dotenv
from os import environ

load_dotenv()


class Config:
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')
