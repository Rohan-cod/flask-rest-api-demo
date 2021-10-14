#! /usr/bin/env python3

"""
A Sample REST API Implementation using FLASK.
Run `Python3 main.py` in your terminal.
Test the API using the curl examples provided in another terminal.
"""

# imports
from flask import Flask, jsonify, abort, request, make_response, url_for
import json
import os

# Initialize a Flask Application
app = Flask(__name__)

# Error Handlers  
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({ 'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({ 'error': 'Not found'}), 404)


# Database; For the sake of this example - A JSON File.
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "wrestlers.json")
with open(filename) as json_file:
    wrestlers = json.load(json_file)


# Return the 'wrestler' JSON with uri instead of the id.
def replace_id_with_uri(wrestler):
    new_wrestler = {}
    for field in wrestler:
        if field == 'id':
            new_wrestler['uri'] = url_for('get_wrestler', wrestler_id = wrestler['id'], _external = True)
        else:
            new_wrestler[field] = wrestler[field]
    return new_wrestler

 
# GET - all
# EXAMPLE: curl -i http://localhost:5000/wwe/api/v1.0/wrestlers
# EXAMPLE: curl -i https://flask-wwe-demo.herokuapp.com/wwe/api/v1.0/wrestlers
@app.route('/wwe/api/v1.0/wrestlers', methods = ['GET'])
def get_wrestlers():
    return jsonify({'wrestlers': list(map(replace_id_with_uri, wrestlers))})


# GET - a specific object
# EXAMPLE: curl -i http://localhost:5000/wwe/api/v1.0/wrestlers/1
@app.route('/wwe/api/v1.0/wrestlers/<int:wrestler_id>', methods = ['GET'])
def get_wrestler(wrestler_id):
    wrestler = list(filter(lambda t: t['id'] == wrestler_id, wrestlers))
    if len(wrestler) == 0:
        abort(404)
    return jsonify({'wrestler': replace_id_with_uri(wrestler[0])})


# POST
# EXAMPLE: curl -i -H "Content-Type: application/json" -X POST -d '{"name":"John"}' http://localhost:5000/wwe/api/v1.0/wrestlers
# EXAMPLE: curl -i -H "Content-Type: application/json" -X POST -d '{"name":"John"}' https://flask-wwe-demo.herokuapp.com/wwe/api/v1.0/wrestlers
@app.route('/wwe/api/v1.0/wrestlers', methods = ['POST'])
def create_wrestler():
    if not request.json or not 'name' in request.json:
        abort(400)
    wrestler = {
        'id': wrestlers[-1]['id'] + 1,
        'name': request.json['name']
    }
    wrestlers.append(wrestler)
    with open(filename, 'w') as file:
        json.dump(wrestlers, file, indent=4)
    return jsonify({'wrestler': replace_id_with_uri(wrestler)}), 201


# PUT
# EXAMPLE: curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"Brock Lesnar"}' http://localhost:5000/wwe/api/v1.0/wrestlers/1
@app.route('/wwe/api/v1.0/wrestlers/<int:wrestler_id>', methods = ['PUT'])
def update_wrestler(wrestler_id):
    wrestler = list(filter(lambda t: t['id'] == wrestler_id, wrestlers))
    if len(wrestler) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != type(u""):
        abort(400)
    wrestler[0]['name'] = request.json.get('name', wrestler[0]['name'])
    with open(filename, 'w') as file:
        json.dump(wrestlers, file, indent=4)
    return jsonify({'wrestler': replace_id_with_uri(wrestler[0])})


# DELETE
# EXAMPLE: curl -i -X Delete http://localhost:5000/wwe/api/v1.0/wrestlers/3
@app.route('/wwe/api/v1.0/wrestlers/<int:wrestler_id>', methods = ['DELETE'])
def delete_wrestler(wrestler_id):
    wrestler = list(filter(lambda t: t['id'] == wrestler_id, wrestlers))
    if len(wrestler) == 0:
        abort(404)
    wrestlers.remove(wrestler[0])
    with open(filename, 'w') as file:
        json.dump(wrestlers, file, indent=4)
    return jsonify({'result': True})
    
if __name__ == '__main__':
    app.run()
