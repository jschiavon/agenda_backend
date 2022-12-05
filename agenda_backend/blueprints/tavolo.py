from flask import Blueprint, jsonify, request

from agenda_backend.database import db
from agenda_backend.models.tavolo import Tavolo, tavolo_schema, tavoli_schema

tavolo = Blueprint('table', __name__)


@tavolo.route('/table/<id>')
def get_table_data(id):
    try:
        try:
            table = db.session.execute(db.select(Tavolo).filter_by(id=id)).scalar_one()
        except NoResultFound:
            return jsonify({'error': "No tables corresponding to this id"}), 401
        finally:
            return jsonify(tavolo_schema.dump(table))
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@tavolo.route('/table/list/<ristoid>')
def get_table_list(ristoid):
    try:
        try:
            tables = db.session.execute(db.select(Tavolo).filter_by(id_Ristorante=ristoid)).scalars().all()
        except NoResultFound:
            return jsonify({'error': "No tables corresponding to this restaurant id"}), 401
        finally:
            if len(tables) > 0:
                return jsonify(tavoli_schema.dump(tables))
            else:
                return jsonify({'error': "No tables corresponding to this restaurant id"}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400