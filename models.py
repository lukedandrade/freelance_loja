from flask_login import UserMixin
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph
from flask import current_app
from flask_app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    permissions = db.Column(db.Integer)
    username = db.Column(db.String(16), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    id_loja = db.Column(db.Integer, db.ForeignKey('stores.id'))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = gph(password)

    def verify_password(self, password):
        return cph(self.password_hash, password)

class Loja(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(32), index=True, unique=True)

class Produto(db.Model):
    __tablename__ = 'productes'
    id = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, index = True, unique=True)
    prod_name = db.Column(db.String(64), unique=True)
    prod_unit_scale = db.Column(db.String(32))
    prod_value = db.Column(db.Float)
    prod_reserve = db.Column(db.Integer)
    prod_type = db.Column(db.String(16))

class Pedido(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    request = db.Column(db.Text)
    situation = db.Column(db.Integer)