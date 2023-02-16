from flask import Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound

from agenda_backend.database import db
from agenda_backend.models.slot import Slot, slot_schema, slots_schema

slot = Blueprint('slot', __name__)

@slot.route('/slot/<id>')
def get_slot_data(id):
    try:
        try:
            _slot = db.session.execute(db.select(Slot).filter_by(id=id)).scalar_one()
        except NoResultFound:
            return jsonify({'error': "No slot corresponding to this id"}), 401
        finally:
            return jsonify(slot_schema.dump(_slot))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@slot.route('/slot/list/<ristoid>')
def get_slot_list(ristoid):
    try:
        try:
            slots = db.session.execute(db.select(Slot).filter_by(id_Ristorante=ristoid)).scalars().all()
        except NoResultFound:
            return jsonify({'error': "No slots corresponding to this restaurant id"}), 401
        finally:
            if len(slots) > 0:
                return jsonify(slots_schema.dump(slots))
            else:
                return jsonify({'error': "No slots corresponding to this restaurant id"}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@slot.route('/slot/add/', methods=['POST'])
def add_slot():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            ristoid = data['id_Ristorante']
        except KeyError:
            return jsonify({'error': 'Must provide id_Ristorante'}), 400

        try:
            giorno = data['Giorno']
        except KeyError:
            return jsonify({'error': 'Must provide Giorno'}), 400

        try:
            orario = data['Orario']
        except KeyError:
            return jsonify({'error': 'Must provide Orario'}), 400

        _slot = Slot(
            id_Ristorante = ristoid,
            Giorno = giorno,
            Orario = orario
        )
    
        db.session.add(_slot)
        db.session.commit()
        
        return jsonify(slot_schema.dump(_slot))
    
    return jsonify({"error": "Must provide complete data"}), 400

@slot.route('/slot/edit/<id>/', methods=['POST'])
def edit_slot(id):
    try:
        _slot = db.session.execute(db.select(Slot).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No slot corresponding to this id"}), 401

    if request.method == 'POST':
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            _slot.Giorno = data['Giorno']
            _slot.Orario = data['Orario']
        except KeyError:
            return jsonify({'error': 'Must provide complete data'}), 400

        db.session.commit()

        return jsonify(slot_schema.dump(_slot))

    return jsonify({"error": "Must provide complete data"}), 400

@slot.route('/slot/delete/<id>', methods=['DELETE'])
def delete_slot(id):
    try:
        _slot = db.session.execute(db.select(Slot).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No slot corresponding to this id"}), 401

    db.session.delete(_slot)
    db.session.commit()

    return jsonify({'message':'Slot {id} deleted'}), 200