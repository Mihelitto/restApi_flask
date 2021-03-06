from jwt.exceptions import InvalidTokenError
from db import Base, engine, session, User, Message
from flask import Flask, jsonify, request, make_response
from auth_utils import hash_password, create_token, check_token
from config import secret_key


app = Flask(__name__)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


@app.route('/login', methods=["POST"])
def login():
    payload = request.json
    if payload and 'name' in payload and 'password' in payload:
        user = (
            session
            .query(User.name, User.password)
            .filter(User.name==payload['name'])
            .first()
        )
        if user.password == hash_password(payload['password']):
            token = create_token(user['name'], secret_key)
            return make_response(jsonify({'token': token}), 200)
        return make_response(jsonify({'error': 'wrong name or password'}), 401)
    return make_response(jsonify({'error': 'bad request'}), 400)


@app.route('/messages', methods=["POST"])
def messages():
    payload = request.json
    auth_credentials = request.headers.get('Authorization')
    try:
        check_token(auth_credentials, secret_key)
    except (InvalidTokenError, ValueError):
        return make_response(jsonify({'error': 'Unauthorized'}), 401)

    if payload and 'name' in payload and 'message' in payload:
        if 'history' in payload['message']:
            *_, count = payload['message'].split()
            if count.isdigit():
                messages = (session
                            .query(User.name, Message.message)
                            .filter(User.id == Message.user)
                            .order_by(Message.id)
                            .limit(int(count))
                            .all()
                            )
                result = []
                for message in messages:
                    result.append(
                        {'name': message.name, 'message': message.message}
                    )
                return make_response(jsonify(result), 200)
        else:
            username = payload['name']
            user = session.query(User).filter(User.name == username).first()
            new_message = Message(user_id=user.id, message=payload['message'])
            session.add(new_message)
            session.commit()
            return jsonify({'user': user.name, 'message': 'created'})

    return make_response(jsonify({'error': 'bad request'}), 400)


@app.route('/users', methods=["GET", "POST"])
def users():
    if request.method == 'POST':
        payload = request.json
        if payload and 'name' in payload and 'password' in payload:
            user = User(
                name=payload['name'],
                password=hash_password(payload['password'])
            )
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
