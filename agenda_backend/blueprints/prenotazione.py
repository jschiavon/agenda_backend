from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound

from agenda_backend.database import db
from agenda_backend.models.prenotazione import Prenotazione, prenotazione_schema, prenotazioni_schema


prenotazione = Blueprint('reservation', __name__)

@prenotazione.route('/reservations/<id>')
def get_reservation_data(id):
    try:
        try:
            reservation = db.session.execute(db.select(Prenotazione).filter_by(id=id)).scalar_one()
        except NoResultFound:
            return jsonify({'error': "No reservation corresponding to this id"}), 401
        finally:
            return jsonify(prenotazione_schema.dump(reservation))
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@prenotazione.route('/reservations/list/<ristoid>')
def get_reservation_list(ristoid):
    try:
        try:
            reservations = db.session.execute(db.select(Prenotazione).filter_by(id_Ristorante=ristoid)).scalars().all()
        except NoResultFound:
            return jsonify({'error': "No reservations corresponding to this restaurant id"}), 401
        finally:
            if len(reservations) > 0:
                return jsonify(prenotazioni_schema.dump(reservations))
            else:
                return jsonify({'error': "No reservations corresponding to this restaurant id"}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@prenotazione.route('/reservations/add/', methods=['POST'])
def add_reservation():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            ristoid = data['id_Ristorante']
        except KeyError:
            return jsonify({'error': 'Must provide id_Ristorante'}), 400

        try:
            DataOra = data['DataOra']
        except KeyError:
            return jsonify({'error': 'Must provide DataOra'}), 400

        try:
            Tavolo = data['Tavolo']
        except KeyError:
            return jsonify({'error': 'Must provide Tavolo'}), 400

        try:
            Numero_Posti = data['Numero_Posti']
        except KeyError:
            return jsonify({'error': 'Must provide Numero_Posti'}), 400
        
        try:
            id_Cliente = data['id_Cliente']
        except KeyError:
            return jsonify({'error': 'Must provide Id_Cliente'}), 400

        try:
            id_user = data['id_User']
        except KeyError:
            return jsonify({'error': 'Must provide id_User'}), 400

        reservation = Prenotazione(
            id_Ristorante = ristoid,
            DataOra = DataOra,
            Tavolo = Tavolo,
            Numero_Posti = Numero_Posti,
            id_Cliente = id_Cliente,
            Note = data['Note'] if 'Note' in data.keys() else None,
            id_User = id_user,
            DataOra_Prenotazione = datetime.now(),
            Flag_Disdetta = data['Flag_disdetta'] if 'Flag_disdetta' in data.keys() else False
        )
    
        db.session.add(reservation)
        db.session.commit()
        
        return jsonify(prenotazione_schema.dump(reservation))
    
    return jsonify({"error": "Must provide complete data"}), 400



@prenotazione.route('/reservations/edit/<id>/', methods=['POST'])
def edit_reservation(id):
    try:
        reservation = db.session.execute(db.select(Prenotazione).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No reservation corresponding to this id"}), 401

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Must provide complete data"}), 400
        
        try:
            reservation.id_Ristorante = ristoid
            reservation.DataOra = data['DataOra']
            reservation.Tavolo = data['Tavolo']
            reservation.Numero_Posti = data['Numero_Posti']
            reservation.id_Cliente = data['id_Cliente']
            reservation.Note = data['Note'] if 'Note' in data.keys() else None
            reservation.id_User = data['id_User']
            reservation.DataOra_Prenotazione = datetime.now()
            reservation.disdetta = data['Flag_disdetta'] if 'Flag_disdetta' in data.keys() else False
        except KeyError:
            return jsonify({'error': 'Must provide complete data'}), 400

        db.session.add(reservation)
        db.session.commit()

        return jsonify(prenotazione_schema.dump(reservation))

    return jsonify({"error": "Must provide complete data"}), 400


@prenotazione.route('/reservations/delete/<id>', methods=['DELETE'])
def delete_reservation(id):
    try:
        reservation = db.session.execute(db.select(Prenotazione).filter_by(id=id)).scalar_one()
    except NoResultFound:
        return jsonify({'error': "No reservation corresponding to this id"}), 401

    db.session.delete(reservation)
    db.session.commit()

    return jsonify({'message':'Reservation {id} deleted'}), 200