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


@tavolo.route('/tables/add/', methods=['POST'])
def add_tavolo():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            ristoid = data['id_Ristorante']
        except KeyError:
            return jsonify({'error': 'Must provide id_Ristorante'}), 400

        try:
            valido_dal = data['valido_Dal']
        except KeyError:
            return jsonify({'error': 'Must provide valido_Dal'}), 400

        try:
            valido_al = data['valido_Al']
        except KeyError:
            return jsonify({'error': 'Must provide valido_Al'}), 400

        try:
            numero = data['Tavolo_Numero']
        except KeyError:
            return jsonify({'error': 'Must provide Tavolo_Numero'}), 400

        try:
            posti = data['Tavolo_Posti']
        except KeyError:
            return jsonify({'error': 'Must provide Tavolo_Posti'}), 400

        try:
            sala = data['Sala']
        except KeyError:
            return jsonify({'error': 'Must provide Sala'}), 400

        table = Tavolo(
                id_Ristorante = ristoid,
                valido_dal = valido_dal,
                valido_al = valido_al,
                Tavolo_Numero = numero,
                Tavolo_Posti = posti,
                Sala = sala,
                Interno_Esterno = data['Interno_Esterno'] if 'Interno_Esterno' in data.keys() else None,
                Note = data['Note'] if 'Note' in data.keys() else None,
            )
        
        db.session.add(table)
        db.session.commit()
        
        return jsonify(tavolo_schema.dump(table))
    
    return jsonify({"error": "Must provide complete data"}), 400


@tavolo.route('/tables/edit/<id>', methods=['POST'])
def edit_tavolo(id):
    try:
        table = db.session.execute(db.select(Tavolo).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No tables corresponding to this id"}), 401

    
    if request.method == 'POST':
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            table.id_Ristorante = data['id_Ristorante']
            table.valido_dal = data['valido_Dal']
            table.valido_al = data['valido_Al']
            table.Tavolo_Numero = data['Tavolo_Numero']
            table.Tavolo_Posti = data['Tavolo_Posti']
            table.Sala = data['Sala']
            table.Interno_Esterno = data['Interno_Esterno'] if 'Interno_Esterno' in data.keys() else None
            table.Note = data['Note'] if 'Note' in data.keys() else None
        except KeyError:
            return jsonify({'error': 'Must provide complete data'}), 400
        
        db.session.commit()
        
        return jsonify(tavolo_schema.dump(table))
    
    return jsonify({"error": "Must provide complete data"}), 400


@tavolo.route('/tables/delete/<id>', methods=['DELETE'])
def delete_tavolo(id):
    try:
        table = db.session.execute(db.select(Tavolo).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No tables corresponding to this id"}), 401

    db.session.delete(table)
    db.session.commit()

    return jsonify({'message':'Table {id} deleted'}), 200