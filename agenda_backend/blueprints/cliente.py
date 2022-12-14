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


@cliente.route('/clients/add/', methods=['POST'])
def add_client():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            ristoid = data['id_Ristorante']
        except KeyError:
            return jsonify({'error': 'Must provide id_Ristorante'}), 400

        try:
            nome = data['Nome']
        except KeyError:
            return jsonify({'error': 'Must provide Nome'}), 400

        try:
            cell = data['Cell']
        except KeyError:
            return jsonify({'error': 'Must provide Cell'}), 400

        try:
            id_user = data['id_User']
        except KeyError:
            return jsonify({'error': 'Must provide id_User'}), 400

        client = Cliente(
            id_Ristorante = ristoId,
            Nome = nome,
            Cell = cell,
            Email = data['Email'] if 'Email' in data.keys() else None,
            Compleanno = data['Compleanno'] if 'Compleanno' in data.keys() else None,
            Note = data['Note'] if 'Note' in data.keys() else None,
            id_User_Creazione = id_user,
            Data_Creazione = datetime.now()
        )
        
        db.session.add(client)
        db.session.commit()
        
        return jsonify(cliente_schema.dump(client))
    
    return jsonify({"error": "Must provide complete data"}), 400


@cliente.route('/clients/edit/<id>/', methods=['POST'])
def edit_client(id):
    try:
        client = db.session.execute(db.select(Cliente).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No clients corresponding to this id"}), 401

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            client.id_Ristorante = data['id_Ristorante']
            client.Nome = data['Nome']
            client.Cell = data['Cell']
            client.Email = data['Email'] if 'Email' in data.keys() else None,
            client.Compleanno = data['Compleanno'] if 'Compleanno' in data.keys() else None,
            client.Note = data['Note'] if 'Note' in data.keys() else None,
            client.id_User_Creazione = data['id_User']
        except KeyError:
            return jsonify({'error': 'Must provide complete data'}), 400

        db.session.add(client)
        db.session.commit()

        return jsonify(cliente_schema.dump(client))

    return jsonify({"error": "Must provide complete data"}), 400


@cliente.route('/clients/delete/<id>', methods=['DELETE'])
def delete_cliente(id):
    try:
        client = db.session.execute(db.select(Cliente).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No clients corresponding to this id"}), 401

    db.session.delete(client)
    db.session.commit()

    return jsonify({'message':'Client {id} deleted'}), 200