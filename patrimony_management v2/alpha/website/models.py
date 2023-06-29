from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class Token(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(150), unique=True)
    timestamp = db.Column(db.DateTime)

class Cliente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mod_time = db.Column(db.DateTime)
    name = db.Column(db.String(150))
    cpf = db.Column(db.String(150))
    birthday = db.Column(db.DateTime)
    civil_state = db.Column(db.String(150))
    email = db.Column(db.String(150))
    phone = db.Column(db.String(150))
    address = db.Column(db.String(150))
    occupation = db.Column(db.String(150))
    workplace = db.Column(db.String(150))
    investor_profile = db.Column(db.String(150))
    txt_dict_1 = db.Column(db.String(150))
    txt_dict_2 = db.Column(db.String(150))
    txt_dict_3 = db.Column(db.String(150))
    txt_dict_4 = db.Column(db.String(150))
    txt_dict_5 = db.Column(db.String(150))
    txt_dict_6 = db.Column(db.String(150))
    txt_dict_7 = db.Column(db.String(150))
    txt_dict_8 = db.Column(db.String(150))
    txt_dict_9 = db.Column(db.String(150))
    txt_dict_10 = db.Column(db.String(150))
    txt_dict_11 = db.Column(db.String(150))
    txt_dict_12 = db.Column(db.String(150))
    txt_dict_13 = db.Column(db.String(150))
    txt_dict_14 = db.Column(db.String(150))
    txt_dict_15 = db.Column(db.String(150))
    txt_dict_16 = db.Column(db.String(150))
    txt_dict_17 = db.Column(db.String(150))

    cliente = relationship('User', backref='cliente')

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    name = db.Column(db.String(150))
    parenthood = db.Column(db.String(150))
    birthday = db.Column(db.DateTime)
    marriage = db.Column(db.String(150))

    cliente = relationship('Cliente', backref='family')

class Assets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    asset_name = db.Column(db.String(150))
    asset_class = db.Column(db.String(150))
    asset_value = db.Column(db.Float)
    bank = db.Column(db.String(150))

    cliente = relationship('Cliente', backref='assets')

class Finance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    patrFin = db.Column(db.String(150))
    patrImb = db.Column(db.String(150))
    totalPatr = db.Column(db.Float)
    saving = db.Column(db.String(150))
    income = db.Column(db.String(150))
    expenses = db.Column(db.String(150))

    cliente = relationship('Cliente', backref='finance')

class Objectives(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    objective = db.Column(db.String(150))
    value = db.Column(db.String(150))
    time = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    initValue = db.Column(db.Float)
    monthValue = db.Column(db.Float)
    realValue = db.Column(db.Float)
    actPlan = db.Column(db.String(150))

    cliente = relationship('Cliente', backref='objectives')

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    retAge = db.Column(db.Integer)
    desIncome = db.Column(db.Float)
    initCont = db.Column(db.Float)
    monthCont = db.Column(db.Float)
    realCont = db.Column(db.Float)
    indepActPlan = db.Column(db.String(150))
    
    cliente = relationship('Cliente', backref='investment')
