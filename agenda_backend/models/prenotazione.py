from agenda_backend.database import db


class Prenotazione(db.Model):

    __tablename__ = 'PTR_Prenotazioni'

    id = db.Column(db.Integer, primary_key=True)
    id_Ristorante = db.Column(db.Integer, nullable=False)
    DataOra = db.Column(db.datetime, nullable=False)
    Tavolo= db.Column(db.Integer, nullable=False)
    Numero_Posti = db.Column(db.Integer, nullable=False)
    id_Cliente = db.Column(db.Integer, nullable=False)
    Note = db.Column(db.String, nullable=True)
    id_User = db.Column(db.Integer, nullable=False)
    DataOra_Prenotazione = db.Column(db.datetime, nullable=False)
    Flag_Disdetta = db.Column(db.Boolean, nullable=True)        #<------- eventualmente si può fare come stringa si/no
