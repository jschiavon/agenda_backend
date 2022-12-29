from agenda_backend.database import db
from marshmallow import Schema, fields


class Utente(db.Model):

    __tablename__ = 'PTR_Utenti'

    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String, unique=True, nullable=False)
    Password = db.Column(db.String, nullable=False)
    Nome_Operatore = db.Column(db.String, nullable=False)
    Nome_Ristorante = db.Column(db.String, nullable=False)
    Indirizzo = db.Column(db.String, nullable=False)
    Cap = db.Column(db.String(5), nullable=False)
    Localita = db.Column(db.String, nullable=False)
    Provincia = db.Column(db.String(2), nullable=False)
    Telefono = db.Column(db.String(13), nullable=False)
    Email = db.Column(db.String, nullable=False)
    Locale = db.Column(db.String(2), nullable=False)
    Note =  = db.Column(db.String, nullable=True)


class __UtenteSchema(Schema):
    id = fields.Int(dump_only=True)
    Username = fields.Str()
    Password = fields.Str()
    Nome_Operatore = fields.Str()
    Nome_Ristorante = fields.Str()
    Indirizzo = fields.Str()
    Cap = fields.Str()
    Localita = fields.Str()
    Provincia = fields.Str()
    Telefono = fields.Str()
    Email = fields.Str()
    Locale = fields.Str()
    Note = fields.Str()

utente_schema = __UtenteSchema()
