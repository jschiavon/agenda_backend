from flask import Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound

from agenda_backend.database import db
from agenda_backend.models.sala import Sala, sala_schema, sale_schema

sala = Blueprint('room', __name__)

@sala.route('/rooms/list/<ristoid>')
def get_rooms_list(ristoid):
    try:
        try:
            rooms = db.session.execute(db.select(Sala).filter_by(id_Ristorante=ristoid)).scalars().all()
        except NoResultFound:
            return jsonify({'error': "No rooms corresponding to this restaurant id"}), 401
        finally:
            if len(rooms) > 0:
                return jsonify(sale_schema.dump(rooms))
            else:
                return jsonify({'error': "No rooms corresponding to this restaurant id"}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@sala.route('/rooms/add/', methods=['POST'])
def add_room():
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
            numero = data['numero']
        except KeyError:
            return jsonify({'error': 'Must provide numero'}), 400

        try:
            colore = data['colore']
        except KeyError:
            return jsonify({'error': 'Must provide Tavolo_Posti'}), 400

        room = Sala(
            id_Ristorante = ristoid,
            valido_dal = valido_dal,
            valido_al = valido_al,
            numero = numero,
            colore = colore,
            Interno_Esterno = data['Interno_Esterno'] if 'Interno_Esterno' in data.keys() else None,
            Note = data['Note'] if 'Note' in data.keys() else None,
        )
        
        db.session.add(room)
        db.session.commit()
        
        return jsonify(sala_schema.dump(room))
    
    return jsonify({"error": "Must provide complete data"}), 400


@sala.route('/rooms/edit/<id>/', methods=['POST'])
def edit_room(id):
    try:
        room = db.session.execute(db.select(Sala).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No rooms corresponding to this id"}), 401

    if request.method == 'POST':
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            room.id_Ristorante = data['id_Ristorante']
            room.valido_dal = data['valido_Dal']
            room.valido_al = data['valido_Al']
            room.numero = data['numero']
            room.colore = data['colore']
            room.Interno_Esterno = data['Interno_Esterno'] if 'Interno_Esterno' in data.keys() else None
            room.Note = data['Note'] if 'Note' in data.keys() else None
        except KeyError:
            return jsonify({'error': 'Must provide complete data'}), 400

        db.session.commit()

        return jsonify(sala_schema.dump(room))

    return jsonify({"error": "Must provide complete data"}), 400


@sala.route('/rooms/delete/<id>', methods=['DELETE'])
def delete_room(id):
    try:
        room = db.session.execute(db.select(Sala).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No rooms corresponding to this id"}), 401

    db.session.delete(room)
    db.session.commit()

    return jsonify({'message':'Room {id} deleted'}), 200