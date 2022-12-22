from agenda_backend.database import db
from marshmallow import Schema, fields


class Sala(db.Model):

    __tablename__ = 'PTR_Sale'

    id = db.Column(db.Integer, primary_key=True)
    id_Ristorante = db.Column(db.Integer, nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    valido_dal = db.Column(db.Date, nullable=False)
    valido_al = db.Column(db.Date, nullable=False)
    colore = db.Column(db.String(10), nullable=False)
    Interno_Esterno = db.Column(db.Boolean, nullable=True)
    Note = db.Column(db.String, nullable=True)
    

class __SalaSchema(Schema):
    id = fields.Int(dump_only=True)
    id_Ristorante = fields.Int()
    numero = fields.Int()
    valido_dal = fields.Date()
    valido_al = fields.Date()
    colore = fields.Str(10)
    Interno_Esterno = fields.Bool()
    Note = fields.Str()
    

sala_schema = __SalaSchema()
sale_schema = __SalaSchema(many=True)