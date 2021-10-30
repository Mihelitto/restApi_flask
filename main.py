from db import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify, request
import base64

app = Flask(__name__)

engine = create_engine(
    'sqlite:///db.sqlite3?check_same_thread=False'
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.route('/login', methods=["GET", "POST"])
def login():
    
    payload = request.json
    if 'name' in payload:
        print(payload['name'], payload['password'])
        token = base64.b64encode(bytes(payload['name']))
        return jsonify({'token': token})


@app.route('/users', methods=["GET", "POST"])
def users():
    if request.method == 'POST':
        payload = request.json
        if 'name' in payload:
            user = User(name=payload['name'], password=payload['password'])
            session.add(user)
            session.commit()
            return jsonify({'user': user.name, 'created': True})
        return jsonify({'error': 'wrong parameters'})
        
    elif request.method == 'GET':
        users = session.query(User.name, User.password).all()
        result = []
        for user in users:
            result.append({'name': user.name, 'password': user.password})
        return jsonify(result)
            
    return jsonify({'error': 'wrong method'})
    

if __name__ == '__main__':
    app.run(debug=True)
