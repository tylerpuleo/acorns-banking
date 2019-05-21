"""
Author: Tyler Puleo
License: GPL
Version: 0.0.1
Maintainer: Tyler Puleo
Status: Production
Summary: This is the models file where all database models are defined.
"""

from app import db
from datetime import datetime
from sqlalchemy_utils import ChoiceType, EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

secret_key = "F21998729FE5D4BCCE8A4FAADE659"


class Customers(db.Model):
    __tablename__ = "Customers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(EncryptedType(db.String(), secret_key, AesEngine, 'pkcs5'))
    last_name = db.Column(EncryptedType(db.String(), secret_key, AesEngine, 'pkcs5'))
    phone_number = db.Column(EncryptedType(db.String(), secret_key, AesEngine, 'pkcs5'))  # Must be of format ###-###-####
    email = db.Column(EncryptedType(db.String(), secret_key, AesEngine, 'pkcs5'))  # Must be of farmat abc@qrs.xyz
    ssn = db.Column(EncryptedType(db.String(11), secret_key, AesEngine, 'pkcs5'))  # Must be of format ###-##-####
    active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, first_name, last_name, phone_number, email, ssn, active):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.ssn = ssn
        self.active = active

    def __repr__(self):
        return '<id {}, name {} {}>'.format(self.id, self.first_name, self.last_name)

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'ssn': self.ssn,
            'active': self.active,
            'created_at': self.created_at
        }


class Accounts(db.Model):
    __tablename__ = "Accounts"

    account_types_choices = {
        ("checking", "checking"),
        ("savings", "savings"),
        ("mortgage", "mortgage"),
        ("retirement", "retirement"),
        ("investing", "investing")

    }

    status_choices = {
        ("opened", "opened"),
        ("closed", "closed"),
        ("locked", "locked"),
        ("abandoned", "abandoned")

    }

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("Customers.id"))
    customer = db.relationship("Customers")
    account_type = db.Column(ChoiceType(account_types_choices))
    balance = db.Column(db.Float())
    account_number = db.Column(db.String(), unique=True)
    routing_number = db.Column(db.String())
    status = db.Column(ChoiceType(status_choices))
    active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, customer, customer_id, account_type, balance, account_number, routing_number, status, active):
        self.customer_id = customer_id
        self.customer = customer
        self.account_type = account_type
        self.balance = balance
        self.account_number = account_number
        self.routing_number = routing_number
        self.status = status
        self.active = active

    def __repr__(self):
        return '<id {}, account number {}>'.format(self.id, self.account_number)

    def serialize(self):
        return {
            'id': self.id,
            'account_type': self.account_type.value,
            'balance': self.balance,
            'account_number': self.account_number,
            'routing_number': self.routing_number,
            'status': self.status.value,
            'active': self.active,
            'created_at': self.created_at
        }


class Ledger(db.Model):
    __tablename__ = "Ledger"

    transaction_type_choices = {
        ("debit", "debit"),
        ("credit", "credit")
    }

    details_choices = {
        ("debit_card_purchase", "debit_card_purchase"),
        ("direct_deposit", "direct_deposit"),
        ("transfer_in", "transfer_in"),
        ("cashed_check", "cashed_check"),
        ("transfer_away", "transfer_away"),
        ("cash_deposit", "cash_deposit")
    }

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("Accounts.id"))
    account = db.relationship("Accounts")
    transaction_type = db.Column(ChoiceType(transaction_type_choices))
    amount = db.Column(db.Float())
    details = db.Column(ChoiceType(details_choices))
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, account_id, account, transaction_type, amount, details):
        self.account_id = account_id
        self.account = account
        self.transaction_type = transaction_type
        self.amount = amount
        self.details = details

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'transaction_type': self.transaction_type.value,
            'amount': self.amount,
            'details': self.details.value,
            'created_at': self.created_at,
        }
