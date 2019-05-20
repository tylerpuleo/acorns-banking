from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from sqlalchemy import or_

app = Flask(__name__)
api = Api(app)

app.config.from_object("config.ProductionConfig")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Customers, Accounts, Ledger


@app.route("/")
def hello():
    return "Welcome to Tyler's Banking API"


class CustomersIndexController(Resource):
    def get(self):
        try:
            customers = Customers.query.all()

            return jsonify([a_customer.serialize() for a_customer in customers])

        except Exception as e:
            return(str(e))

    def post(self):

        try:
            print request.values
            customer = Customers(
                first_name=request.values['first_name'],
                last_name=request.values['last_name'],
                phone_number=request.values['phone_number'],
                email=request.values['email'],
                ssn=request.values['ssn'],
                active=bool(request.values['active']),
            )

            db.session.add(customer)
            db.session.commit()

            return jsonify(customer.serialize())

        except Exception as e:
            return(str(e))


class CustomersController(Resource):
    def get(self, customer_id):
        try:
            customer = Customers.query.filter_by(id=customer_id).first()
            return jsonify(customer.serialize())

        except Exception as e:
            return(str(e))

    def put(self, customer_id):
        try:
            customer = Customers.query.filter_by(id=customer_id).first()

            customer.first_name = request.values['first_name'] if "first_name" in request.values else customer.first_name
            customer.last_name = request.values['last_name'] if "last_name" in request.values else customer.last_name
            customer.phone_number = request.values['phone_number'] if "phone_number" in request.values else customer.phone_number
            customer.email = request.values['email'] if "email" in request.values else customer.email
            customer.ssn = request.values['ssn'] if "ssn" in request.values else customer.ssn
            customer.active = bool(request.values['active']) if "active" in request.values else customer.active

            db.session.commit()

            return jsonify(customer.serialize())

        except Exception as e:
            return(str(e))


class AccountsIndexController(Resource):
    def get(self, customer_id):
        try:
            accounts = db.session.query(Customers, Accounts).outerjoin(Accounts).filter(Accounts.customer_id == Customers.id).all()

            return jsonify([account[1].serialize() for account in accounts])

        except Exception as e:
            return(str(e))

    def post(self, customer_id):
        customer = Customers.query.filter_by(id=customer_id).first()
        print customer
        try:
            account = Accounts(
                customer=customer,
                customer_id=customer.id,
                account_type=request.values['account_type'],
                balance=request.values['balance'],
                account_number=request.values['account_number'],
                routing_number=request.values['routing_number'],
                status=request.values['status'],
                active=bool(request.values['active'])
            )
            db.session.add(account)
            db.session.commit()

            return jsonify(account.serialize())

        except Exception as e:
            return(str(e))


class AccountsController(Resource):
    def get(self, customer_id, account_id):
        try:

            account = db.session.query(Customers, Accounts).outerjoin(Accounts).filter(Accounts.customer_id == Customers.id, Accounts.id == account_id).all()[0][1]

            return jsonify(account.serialize())

        except Exception as e:
            return(str(e))

    def put(self, customer_id, account_id):
        try:
            account = Accounts.query.filter_by(customer_id=customer_id, id=account_id).first()

            account.account_type = request.values['account_type'] if "account_type" in request.values else account.account_type
            account.balance = request.values['balance'] if "balance" in request.values else account.balance
            account.account_number = request.values['account_number'] if "account_number" in request.values else account.account_number
            account.routing_number = request.values['routing_number'] if "routing_number" in request.values else account.routing_number
            account.status = request.values['status'] if "status" in request.values else account.status
            account.active = bool(request.values['active']) if "active" in request.values else account.active

            db.session.commit()

            return jsonify(account.serialize())

        except Exception as e:
            return(str(e))


class LedgerController(Resource):
    def get(self, customer_id, account_id):
        try:
            ledger = db.session.query(Customers, Accounts, Ledger).outerjoin(Ledger).filter(Accounts.customer_id == Customers.id).filter(Ledger.account_id == account_id).all()
            return jsonify([l[2].serialize() for l in ledger])

        except Exception as e:
            return(str(e))


class TransferController(Resource):
    def post(self, customer_id):
        try:
            to_account_id = request.values['to_account_id']
            from_account_id = request.values['from_account_id']
            amount = request.values['amount']

            to_account = db.session.query(Customers, Accounts).outerjoin(Accounts).filter(Accounts.customer_id == Customers.id, Accounts.id == to_account_id).all()[0][1]
            from_account = db.session.query(Customers, Accounts).outerjoin(Accounts).filter(Accounts.customer_id == Customers.id, Accounts.id == from_account_id).all()[0][1]

            ledger_credit = Ledger(
                account_id=to_account_id,
                account=to_account,
                transaction_type="credit",
                amount=amount,
                details="transfer_in",
            )
            db.session.add(ledger_credit)
            db.session.commit()

            ledger_debit = Ledger(
                account_id=from_account_id,
                account=from_account,
                transaction_type="debit",
                amount=amount,
                details="transfer_away",
            )
            db.session.add(ledger_debit)

            db.session.commit()

            return_json = {
                "to_account": to_account_id,
                "from_account": from_account_id,
                "amount": amount
            }

            return jsonify(return_json)

        except Exception as e:
            return(str(e))


api.add_resource(CustomersIndexController, '/customers')
api.add_resource(CustomersController, '/customers/<string:customer_id>')
api.add_resource(AccountsIndexController, '/customers/<string:customer_id>/accounts')
api.add_resource(AccountsController, '/customers/<string:customer_id>/accounts/<string:account_id>')
api.add_resource(LedgerController, '/customers/<string:customer_id>/accounts/<string:account_id>/ledger')
api.add_resource(TransferController, '/customers/<string:customer_id>/transfer')


if __name__ == '__main__':
    app.run()
