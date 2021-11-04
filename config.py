import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "You will never guess..."
    SQLALCHEMY_DATABASE_URI = "DEPLOY_DATABASE_URL"
    SQLALCHEMY_TRACK_MODIFICATIONS = False