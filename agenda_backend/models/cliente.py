from agenda_backend.database import db
from marshmallow import Schema, fields


class Cliente(db.Model):

    __tablename__ = 'PTR_Clienti'

    id = db.Column(db.Integer, primary_key=True)
    id_Ristorante = db.Column(db.Integer, nullable=False)
    Nome = db.Column(db.String, nullable=False)
    Cell = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=True)
    Compleanno = db.Column(db.Date, nullable=True)
    Note = db.Column(db.String, nullable=True)
    id_User_Creazione = db.Column(db.Integer, nullable=False)
    Data_Creazione = db.Column(db.DateTime, nullable=False)


class __ClienteSchema(Schema):
    id = fields.Int(dump_only=True)
    id_Ristorante = fields.Int()
    Nome = fields.Str()
    Cell = fields.Str()
    Email = fields.Str()
    Compleanno = fields.Date()
    Note = fields.Str()
    id_User_Creazione = fields.Int()
    Data_Creazione = fields.DateTime()


cliente_schema = __ClienteSchema()
clienti_schema = __ClienteSchema(many=True)