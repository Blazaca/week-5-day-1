import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "You will never guess..."
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:NKd#!a$Ff58X@localhost:5432/synth_inventory"
    SQLALCHEMY_TRACK_MODIFICATIONS = False