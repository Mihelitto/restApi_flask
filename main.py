from db import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify, request, make_response
from auth_utils import hash_password, create_token


secret_key = "kjldfjsfgpo"


app = Flask(__name__)

engine = create_engine(
    'sqlite:///db.sqlite3?check_same_thread=False'
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        payload = request.json
        if payload and 'name' in payload and 'password' in payload:
            user = session.query(User.name, User.password).filter(User.name==payload['name']).first()
            if user.password == hash_password(payload['password']):
                token = create_token(user["name"], secret_key)
                return make_response(jsonify({'token': token}), 200)
            return make_response(jsonify({'error': 'wrong name or password'}), 401)
        return make_response(jsonify({'error': 'bad request'}), 400)


@app.route('/users', methods=["GET", "POST"])
def users():
    if request.method == 'POST':
        payload = request.json
        if payload and 'name' in payload and 'password' in payload:
            user = User(name=payload['name'], password=payload['password'])
            session.add(user)
            session.commit()
            return jsonify({'user': user.name, 'created': True})
        
    elif request.method == 'GET':
        users = session.query(User.name, User.password).all()
        result = []
        for user in users:
            result.append({'name': user.name, 'password': user.password})
        return make_response(jsonify(result), 200)
            
    return make_response(jsonify({'error': 'bad request'}), 400)
    

if __name__ == '__main__':
    app.run(debug=True)
