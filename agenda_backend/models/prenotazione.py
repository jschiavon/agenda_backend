from agenda_backend.database import db
from marshmallow import Schema, fields


class Prenotazione(db.Model):

    __tablename__ = 'PTR_Prenotazioni_var'

    id = db.Column(db.Integer, primary_key=True)
    id_Ristorante = db.Column(db.Integer, nullable=False)
    Data = db.Column(db.Date, nullable=False)
    Slots = db.Column(db.String, nullable=False)
    Tavolo= db.Column(db.Integer, nullable=False)
    Numero_Posti = db.Column(db.Integer, nullable=False)
    id_Cliente = db.Column(db.Integer, nullable=False)
    Note = db.Column(db.String, nullable=True)
    DataOra_Prenotazione = db.Column(db.DateTime, nullable=False)
    Flag_Disdetta = db.Column(db.Boolean, nullable=True)


class __PrenotazioneSchema(Schema):
    id = fields.Int(dump_only=True)
    id_Ristorante = fields.Int()
    Data = fields.Date()
    Slots = fields.Str()
    Tavolo= fields.Int()
    Numero_Posti = fields.Int()
    id_Cliente = fields.Int()
    Note = fields.Str()
    DataOra_Prenotazione = fields.DateTime()
    Flag_Disdetta = fields.Bool()


prenotazione_schema = __PrenotazioneSchema()
prenotazioni_schema = __PrenotazioneSchema(many=True)