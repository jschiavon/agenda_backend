from flask import Flask
from flask_cors import CORS

from agenda_backend.database import db
from agenda_backend.blueprints.utente import utente
from agenda_backend.blueprints.tavolo import tavolo
from agenda_backend.blueprints.cliente import cliente
from agenda_backend.blueprints.prenotazione import prenotazione
from agenda_backend.blueprints.sala import sala
from agenda_backend.blueprints.slot import slot


def create_app(*args, **kwargs):
    env = kwargs['env']
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.%s' % env)
    app.register_blueprint(utente)
    app.register_blueprint(tavolo)
    app.register_blueprint(cliente)
    app.register_blueprint(prenotazione)
    app.register_blueprint(sala)
    app.register_blueprint(slot)
    db.init_app(app)
    return app