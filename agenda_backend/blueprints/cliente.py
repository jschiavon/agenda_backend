from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound

from agenda_backend.database import db
from agenda_backend.models.cliente import Cliente, cliente_schema, clienti_schema

cliente = Blueprint('client', __name__)


@cliente.route('/clients/<id>')
def get_client_data(id):
    try:
        try:
            client = db.session.execute(db.select(Cliente).filter_by(id=id)).scalar_one()
        except NoResultFound:
            return jsonify({'error': "No clients corresponding to this id"}), 401
        finally:
            return jsonify(cliente_schema.dump(client))
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@cliente.route('/clients/list/<ristoid>')
def get_clients_list(ristoid):
    try:
        try:
            clients = db.session.execute(db.select(Cliente).filter_by(id_Ristorante=ristoid)).scalars().all()
        except NoResultFound:
            return jsonify({'error': "No clients corresponding to this restaurant id"}), 401
        finally:
            if len(clients) > 0:
                return jsonify(clienti_schema.dump(clients))
            else:
                return jsonify({'error': "No clients corresponding to this restaurant id"}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@cliente.route('/clients/create/<ristoid>', methods=['GET', 'POST'])
def add_client(ristoid):
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            client = Cliente(
                id_Ristorante = ristoid,
                Nome = nome,
                Cell = cell,
                Email = data['email'] if 'email' in data.keys() else None,
                Compleanno = data['compleanno'] if 'compleanno' in data.keys() else None,
                Note = data['note'] if 'note' in data.keys() else None,
                id_User_Creazione = id_User_Creazione,
                Data_Creazione = datetime.now()
            )
        except KeyError:
            return jsonify({'error': 'Must provide complete data'}), 400

        db.session.add(client)
        db.session.commit()
        
        return jsonify(cliente_schema.dump(client))
    
    return jsonify({"error": "Must provide complete data"}), 400


@cliente.route('/clients/<id>/edit/', methods=['GET', 'POST'])
def edit_client():
    try:
        client = db.session.execute(db.select(Cliente).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No clients corresponding to this id"}), 401

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            id_Ristorante = data['ristoid']
        except KeyError:
            return jsonify({"error": "No ristoid provided"}), 400
        
        try:
            nome = data['nome']
        except KeyError:
            return jsonify({"error": "No nome provided"}), 400
        
        try:
            cell = data['cell']
        except KeyError:
            return jsonify({"error": "No cell provided"}), 400
        
        try:
            id_User_Creazione = data['user_id_creazione']
        except KeyError:
            return jsonify({'error': 'No user_id_creazione provided'}), 400

        client.id_Ristorante = id_Ristorante
        client.Nome = nome
        client.Cell = cell
        client.Email = data['email'] if 'email' in data.keys() else None,
        client.Compleanno = data['compleanno'] if 'compleanno' in data.keys() else None,
        client.Note = data['note'] if 'note' in data.keys() else None,
        client.id_User_Creazione = id_User_Creazione

        db.session.add(client)
        db.session.commit()

        return jsonify(cliente_schema.dump(client))

    return jsonify({"error": "Must provide complete data"}), 400