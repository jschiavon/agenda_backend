from flask import Blueprint, jsonify, request

from agenda_backend.database import db
from agenda_backend.models.cliente import Cliente, cliente_schema, clienti_schema

cliente = Blueprint('client', __name__)


@cliente.route('/clients/<id>')
def get_client_data(id):
    try:
        try:
            cliente = db.session.execute(db.select(Cliente).filter_by(id=id)).scalar_one()
        except NoResultFound:
            return jsonify({'error': "No clients corresponding to this id"}), 401
        finally:
            return jsonify(cliente_schema.dump(cliente))
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