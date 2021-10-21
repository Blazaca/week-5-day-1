from flask import Blueprint, request, jsonify
from synth_inventory.helpers import token_required
from synth_inventory.models import Synth, db, synth_schema, synths_schema
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 'coding temple'}

@api.route('/synths', methods=['POST'])
@token_required
def create_synth(current_user_token):
    synth_name = request.json['synth_name']
    description = request.json['description']
    midi_ports = request.json['midi_ports']
    synthesis_type = request.json['synthesis_type']
    voices = request.json['voices']
    file_type = request.json['file_type']
    category = request.json['category']
    user_token = current_user_token.token

    print(f'TEST: {current_user_token.token}')

    synth = Synth(synth_name,description,midi_ports,synthesis_type,voices,file_type,category,user_token)

    db.session.add(synth)
    db.session.commit()

    response = synth_schema.dump(synth)
    return jsonify(response)

@api.route('/synths', methods=['GET'])
@token_required
def get_synths(current_user_token):
    owner = current_user_token.token
    synths = Synth.query.filter_by(user_token = owner).all()
    response = synths_schema.dump(synths)
    return jsonify(response)

@api.route('/synths/<id>', methods=['GET'])
@token_required
def get_synth(current_user_token, id):
    synth = Synth.query.get(id)
    print(f'Here is your Synth: {synth.synth_name}')
    response = synth_schema.dump(synth)
    return jsonify(response)

@api.route('/synths/<id>', methods = ['POST', 'PUT'])
@token_required
def update_synth(current_user_token, id):
    synth = Synth.query.get(id)
    print(synth)
    if synth:
        synth.synth_name = request.json['synth_name']
        synth.description = request.json['description']
        synth.midi_ports = request.json['midi_ports']
        synth.synthesis_type = request.json['synthesis_type']
        synth.voices = request.json['voices']
        synth.file_type = request.json['file_type']
        synth.category = request.json['category']
        synth.user_token = current_user_token.token
        db.session.commit()

        response = synth_schema.dump(synth)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That synth does not exist!'})

@api.route('/synths/<id>', methods = ['DELETE'])
@token_required
def delete_synth(current_user_token, id):
    synth = Synth.query.get(id)
    print(synth)
    if synth:
        db.session.delete(synth)
        db.session.commit()

        return jsonify({'Success': f'Synth ID {synth.id} has been deleted'})
    else:
        return jsonify({'Error': 'That synth does not exist!'})

# 92718b8270bd31104e18b00c76178c1af31eae8aadde946b