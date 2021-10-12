from flask import Flask, request, jsonify
from flask_expects_json import expects_json
from app import app, db
from app.models import User
from flask_login import (
    login_user,
)

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string',  "minLength": 1},
        'email': {'type': 'string', "pattern": "[^@]+@[^@]+\.[^@]"},
        'password': {'type': 'string', "pattern": "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&+=]).*$"}
    },
    'required': ['name', 'email', 'password']
}


@app.route('/api/sign_up', methods=['POST'])
@expects_json(schema)
def sign_up():
    values = request.get_json()
    user = User.query.filter_by(email=values['email']).first()

    if user:
        msg = {'success': False}
        return jsonify(msg), 400
    
    msg = {'success': True}
    user = User(name=values['name'], email=values['email'], password=values['password'])
        
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        msg = {'success': False}
        return jsonify(msg), 400

    return jsonify(msg), 201


@app.route('/api/sign_in', methods=['POST'])
def sign_in():
    values = request.get_json()
    user = User.query.filter_by(email=values['email']).first()

    if user and user.password == values['password']:
        login_user(user)
        msg = {'success': True}
        return jsonify(msg), 200
    
    msg = {'success': False}
    return jsonify(msg), 400


@app.route('/api/clean', methods=['POST'])
def api_clean():
    
    db.session.query(User).delete()
    db.session.commit()
    
    msg = {'success': True}
    return jsonify(msg), 200
    
    

    