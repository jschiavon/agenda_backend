from agenda_backend.database import db
from marshmallow import Schema, fields


class Slot(db.Model):
    __tablename__ = 'PTR_Slot'

    id = db.Column(db.Integer, primary_key=True)
    id_Ristorante = db.Column(db.Integer, nullable=False)
    Giorno = db.Column(db.Integer, nullable=False)
    Orario = db.Column(db.Time, nullable=False)
    

class __SlotSchema(Schema):
    id = fields.Int(dump_only=True)
    id_Ristorante = fields.Int()
    Giorno = fields.Int()
    Orario = fields.Time()
    

slot_schema = __SlotSchema()
slots_schema = __SlotSchema(many=True)