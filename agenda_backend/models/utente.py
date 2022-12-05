from agenda_backend.database import db
from marshmallow import Schema, fields


class Utente(db.Model):

    __tablename__ = 'PTR_Accessi'
    
    id = db.Column(db.Integer, primary_key=True)
    id_Ristorante = db.Column(db.Integer, nullable=False)
    Username = db.Column(db.String, unique=True, nullable=False)
    Password = db.Column(db.String, nullable=False)
    Nome_Operatore = db.Column(db.String, nullable=False)
    Flag_Attivo = db.Column(db.Boolean, nullable=True)
    Note = db.Column(db.String, nullable=True)


class UtenteSchema(Schema):
    id = fields.Int(dump_only=True)
    id_Ristorante = fields.Int()
    Username = fields.Str()
    Password = fields.Str()
    Nome_Operatore = fields.Str()
    Flag_Attivo = fields.Bool()
    Note = fields.Str()


utente_schema = UtenteSchema()