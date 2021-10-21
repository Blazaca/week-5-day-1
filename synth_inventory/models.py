from os import name
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self, length):
        return secrets.token_hex(length)

class Synth(db.Model):
    id = db.Column(db.String, primary_key=True)
    synth_name = db.Column(db.String(150))
    description = db.Column(db.String(250))
    midi_ports = db.Column(db.String(10), nullable = True)
    synthesis_type = db.Column(db.String(50))
    voices = db.Column(db.String(5))
    file_type = db.Column(db.String(25))
    category = db.Column(db.String(50))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, synth_name, description, midi_ports, synthesis_type, voices, file_type, category, user_token, id = ''):
        self.id = self.set_id()
        self.synth_name = synth_name
        self.description = description
        self.midi_ports = midi_ports
        self.synthesis_type = synthesis_type
        self.voices = voices
        self.file_type = file_type
        self.category = category
        self.user_token = user_token

    def set_id(self):
        return(secrets.token_urlsafe())

class SynthSchema(ma.Schema):
    class Meta:
        fields = ['id', 'synth_name', 'description', 'midi_ports', 'synthesis_type', 'voices', 'file_type', 'category', 'user_token']

synth_schema = SynthSchema()
synths_schema = SynthSchema(many=True)

def marshall(synth):
    a_dict = {}
    fields = ['synth_name', 'description', 'midi_ports', 'synthesis_type', 'voices', 'file_type', 'category']
    for field in fields:
        a_dict[field] = synth.field