from agenda_backend.database import db
from marshmallow import Schema, fields


class Tavolo(db.Model):
    __tablename__ = 'PTR_Tavoli'
    
    id = db.Column(db.Integer, primary_key=True)
    id_Ristorante = db.Column(db.Integer, nullable=False)
    valido_dal = db.Column(db.Date, nullable=False)
    valido_al = db.Column(db.Date, nullable=False)
    Tavolo_Numero = db.Column(db.Integer, nullable=False)
    Tavolo_Posti = db.Column(db.Integer, nullable=False)
    Sala = db.Column(db.String, nullable=True)
    Interno_Esterno = db.Column(db.Boolean, nullable=True)        # <------- eventualmente si può fare come stringa si/no
    Note = db.Column(db.String, nullable=True)


class TavoloSchema(Schema):
    id = fields.Int(dump_only=True)
    id_Ristorante = fields.Int()
    valido_dal = fields.Date()
    valido_al = fields.Date()
    Tavolo_Numero = fields.Int()
    Tavolo_Posti = fields.Int()
    Sala = fields.Str()
    Interno_Esterno = fields.Bool()
    Note = fields.Str()
    

tavolo_schema = TavoloSchema()
tavoli_schema = TavoloSchema(many=True)