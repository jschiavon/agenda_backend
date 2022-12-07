from flask import Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound

from agenda_backend.database import db
from agenda_backend.models.tavolo import Tavolo, tavolo_schema, tavoli_schema

tavolo = Blueprint('table', __name__)


@tavolo.route('/tables/<id>')
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


@tavolo.route('/tables/list/<ristoid>')
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


@tavolo.route('/tables/create/<ristoid>', methods=['GET', 'POST'])
def add_tavolo(ristoid):
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            table = Tavolo(
                id_Ristorante = ristoid,
                valido_dal = data['valido_dal'],
                valido_al = data['valido_al'],
                Tavolo_Numero = data['numero'],
                Tavolo_Posti = data['posti'],
                Sala = data['sala'],
                Interno_Esterno = data['interno_esterno'] if 'interno_esterno' in data.keys() else None,
                Note = data['note'] if 'note' in data.keys() else None,
            )
        except KeyError:
            return jsonify({'error': 'Must provide complete data'}), 400
        
        db.session.add(table)
        db.session.commit()
        
        return jsonify(table_schema.dump(table))
    
    return jsonify({"error": "Must provide complete data"}), 400



