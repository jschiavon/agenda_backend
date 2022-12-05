from agenda_backend.database import db


class Ristorante(db.Model):

    __tablename__ = 'PTR_Ristoranti'
    
    id = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String, nullable=False)
    Indirizzo = db.Column(db.String, nullable=True)
    Cap = db.Column(db.String, nullable=True)
    Localita = db.Column(db.String, nullable=True)
    Provincia = db.Column(db.String, nullable=True)
    Tel = db.Column(db.String, nullable=True)
    Email = db.Column(db.String, nullable=True)
    Nome_Responsabile = db.Column(db.String, nullable=True)
    Cell_Responsabile = db.Column(db.String, nullable=True)
    Email_Responsabile = db.Column(db.String, nullable=True)
    Note = db.Column(db.String, nullable=True)