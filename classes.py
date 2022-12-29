from agenda_backend.database import db


class User(db.Model):
    
    __tablename__ = 'PTR_Calendario_Standard'
	
    id = db.Column(db.Integer, primary_key=True)
	id_Ristorante = db.Column(db.Integer, nullable=False)
	valido_dal = db.Column(db.datetime, nullable=False)
	valido_al = db.Column(db.datetime, nullable=False)
	Giorni_Chiusura = db.Column(db.String, nullable=False)
    
    
    __tablename__ = 'PTR_Calendario_Standard_Detail'
    
	id = db.Column(db.Integer, primary_key=True)
	id_master = db.Column(db.Integer, nullable=False)
	feriale_festivo = db.Column(db.String, nullable=False)
	dalle = db.Column(db.datetime, nullable=False)   <---------------- solo time--> ad es. stringa? 'hh:mm'
	alle = db.Column(db.datetime, nullable=False)   <---------------- solo time--> ad es. stringa? 'hh:mm'
    
    
    __tablename__ = 'PTR_Calendario_varianti'
    
	id = db.Column(db.Integer, primary_key=True)
	id_Ristorante = db.Column(db.Integer, primary_key=True)
	giorno = db.Column(db.datetime, nullable=False)
    
    __tablename__ = 'PTR_Calendario_varianti_detail'
    
	id = db.Column(db.Integer, primary_key=True)
	id_master = db.Column(db.Integer, nullable=False)
	dalle_ore = db.Column(db.datetime, nullable=False)   <---------------- solo time--> ad es. stringa? 'hh:mm'
	alle_ore = db.Column(db.datetime, nullable=False)   <---------------- solo time--> ad es. stringa? 'hh:mm'
    
    
 