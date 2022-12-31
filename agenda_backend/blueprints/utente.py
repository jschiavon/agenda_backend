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
        username = data['Username']
    except KeyError as e:
        return jsonify({"error": "No username provided"}), 400
    
    try:
        password = data['Password']
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
    data = request.get_json(force=True)
    if not data:
        return jsonify({'error': 'Must provide the new passowrd'}), 400
    
    try:
        new_password = data['Password']
    except KeyError:
        return jsonify({'error': 'Must provide the new passowrd'}), 400

    try:
        user = db.session.execute(db.select(Utente).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No user corresponding to this id"}), 401
    
    user.Password = generate_password_hash(new_password, 12).decode('latin')

    db.session.commit()

    return jsonify(utente_schema.dump(user))


@utente.route('/user/add/', methods=['POST'])
def add_user():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            username = data['Username']
        except KeyError:
            return jsonify({'error': 'Must provide Username'}), 400

        try:
            password = data['Password']
        except KeyError:
            return jsonify({'error': 'Must provide Password'}), 400
        
        try:
            nome = data['Nome_Operatore']
        except KeyError:
            return jsonify({'error': 'Must provide Nome_Operatore'}), 400

        try:
            nomeRistorante = data['Nome_Ristorante']
        except KeyError:
            return jsonify({'error': 'Must provide Nome_Ristorante'}), 400

        try:
            indirizzo = data['Indirizzo']
        except KeyError:
            return jsonify({'error': 'Must provide Indirizzo'}), 400

        try:
            cap = data['Cap']
        except KeyError:
            return jsonify({'error': 'Must provide Cap'}), 400

        try:
            localita = data['Localita']
        except KeyError:
            return jsonify({'error': 'Must provide Localita'}), 400

        try:
            provincia = data['Provincia']
        except KeyError:
            return jsonify({'error': 'Must provide Provincia'}), 400

        try:
            telefono = data['Telefono']
        except KeyError:
            return jsonify({'error': 'Must provide Telefono'}), 400

        try:
            email = data['Email']
        except KeyError:
            return jsonify({'error': 'Must provide Email'}), 400

        try:
            locale = data['Locale']
        except KeyError:
            return jsonify({'error': 'Must provide Locale'}), 400

        user = Utente(
            Username = username,
            Password = generate_password_hash(password, 12).decode('latin'),
            Nome_Operatore = nome,
            Nome_Ristorante = nomeRistorante,
            Indirizzo = indirizzo,
            Cap = cap,
            Localita = localita,
            Provincia = provincia,
            Telefono = telefono,
            Email = email,
            Locale = locale,
            Note = data['Note'] if 'Note' in data.keys() else None
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify(utente_schema.dump(user))
    
    return jsonify({"error": "Must provide complete data"}), 400


@utente.route('/user/edit/<id>/', methods=['POST'])
def edit_user(id):
    try:
        user = db.session.execute(db.select(Utente).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No users corresponding to this id"}), 401

    if request.method == 'POST':
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        # try:
        #     user.Username = data['Username']
        # except KeyError:
        #     return jsonify({'error': 'Must provide Username'}), 400

        # try:
        #     user.Password = generate_password_hash(data['Password'], 12).decode('latin')
        # except KeyError:
        #     return jsonify({'error': 'Must provide Password'}), 400
        
        try:
            user.Nome_Operatore = data['Nome_Operatore']
        except KeyError:
            return jsonify({'error': 'Must provide Nome_Operatore'}), 400

        try:
            user.Nome_Ristorante = data['Nome_Ristorante']
        except KeyError:
            return jsonify({'error': 'Must provide Nome_Ristorante'}), 400

        try:
            user.Indirizzo = data['Indirizzo']
        except KeyError:
            return jsonify({'error': 'Must provide Indirizzo'}), 400

        try:
            user.Cap = data['Cap']
        except KeyError:
            return jsonify({'error': 'Must provide Cap'}), 400

        try:
            user.Localita = data['Localita']
        except KeyError:
            return jsonify({'error': 'Must provide Localita'}), 400

        try:
            user.Provincia = data['Provincia']
        except KeyError:
            return jsonify({'error': 'Must provide Provincia'}), 400

        try:
            user.Telefono = data['Telefono']
        except KeyError:
            return jsonify({'error': 'Must provide Telefono'}), 400

        try:
            user.Email = data['Email']
        except KeyError:
            return jsonify({'error': 'Must provide Email'}), 400

        try:
            user.Locale = data['Locale']
        except KeyError:
            return jsonify({'error': 'Must provide Locale'}), 400

        user.Note = data['Note'] if 'Note' in data.keys() else None
        
        db.session.commit()
        
        return jsonify(utente_schema.dump(user))
    
    return jsonify({"error": "Must provide complete data"}), 400


@utente.route('/user/check/', methods=['POST'])
def check_username():

    if request.method == 'POST':
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400

        try:
            username = data['username']
        except KeyError:
            return jsonify({'error': 'Must provide username'}), 400

        try:
            user = db.session.execute(db.select(Utente).filter_by(Username=username))..scalars().all()
        except NoResultFound:
            return jsonify({'message': "No users with this username"})
        finally:
            return jsonify({'message': len(rooms)})
            