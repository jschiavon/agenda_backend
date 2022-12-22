from flask import Blueprint, jsonify, request
from flask_bcrypt import check_password_hash, generate_password_hash
from sqlalchemy.exc import NoResultFound

from agenda_backend.database import db
from agenda_backend.models.utente import Utente, utente_schema

utente = Blueprint('user', __name__)

@utente.route('/user/<id>')
def get_user_data(id):
    try:
        try:
            user = db.session.execute(db.select(Utente).filter_by(id=id)).scalar_one()
        except NoResultFound:
            return jsonify({'error': "No user corresponding to this id"}), 401
        finally:
            return jsonify(utente_schema.dump(user))
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@utente.route('/user/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
    except:
        return jsonify({'error': 'Data not in the correct format'}), 400
    if not data:
        return jsonify({"error": "Must provide username and password"}), 400

    try:
        username = data['username']
    except KeyError as e:
        return jsonify({"error": "No username provided"}), 400
    
    try:
        password = data['password']
    except KeyError as e:
        return jsonify({"error": "No password provided"}), 400

    try:
        user = db.session.execute(db.select(Utente).filter_by(Username=username)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No user with this username"}), 401

    if check_password_hash(user.Password, password):
        return jsonify(utente_schema.dump(user))
    else:
        return jsonify({"error": "Password incorrect"}), 401


@utente.route('/user/password/<id>', methods=['POST'])
def change_password(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Must provide the new passowrd'}), 400
    
    try:
        new_password = data['password']
    except KeyError:
        return jsonify({'error': 'Must provide the new passowrd'}), 400

    try:
        user = db.session.execute(db.select(Utente).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No user corresponding to this id"}), 401
    
    user.Password = generate_password_hash(new_password, 12).decode('latin')

    db.session.commit()

    return jsonify(utente_schema.dump(user))
