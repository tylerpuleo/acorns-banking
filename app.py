"""
Author: Tyler Puleo
License: GPL
Version: 0.0.1
Maintainer: Tyler Puleo
Status: Production
Summary: This is the main application code for my api. It contains
         all of the api routes as well as all of the controllers.
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_api import status
from sqlalchemy import or_
from werkzeug.exceptions import BadRequestKeyError

app = Flask(__name__)
api = Api(app)

app.config.from_object("config.ProductionConfig")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Customers, Accounts, Ledger


@app.route("/")
def hello():
    """
    get:
        summary: Endpoint to introduce API.
        parameters:
        responses:
            200:
                Returns welcom string.
    """
    return "Welcome to Tyler's Banking API"


class CustomersIndexController(Resource):
    def get(self):
        """
        get:
            summary: Index controller for customers. Returns all customers
            parameters:
            responses:
                200:
                    Returns array of customer object JSON.
                500:
                    Internal Server Error
        """
        try:
            customers = Customers.query.all()

            # Iterates through each customer returned from the query then
            # constructs an array of the serialized objects and make it JSON.
            return jsonify([a_customer.serialize() for a_customer in customers])

        except Exception as e:
            app.logger.error(str(e))
            return {"error": "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def post(self):
        """
        post:
            summary: Create a new customer
            parameters:
                "first_name": <string>
                "last_name": <string>
                "phone_number": <string>
                "email": <string>
                "ssn": <string>
                "active": <bool>
            responses:
                200:
                    Returns JSON object of the customer object created.
                400:
                    Bad Request: Most likely a param is missing
                500:
                    Internal Server Error
        """
        try:
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

        except BadRequestKeyError as e:
            app.logger.error(str(e))
            return {"error": "Bad Request"}, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            app.logger.error(str(e))
            return {"error": "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR


class CustomersController(Resource):
    def get(self, customer_id):
        """
        get:
            summary: Get a single customer by id.
            parameters:
            responses:
                200:
                    Returns JSON object of the customer object with given id.
                404:
                    Not Found: Customer with given array not found
                500:
                    Internal Server Error
        """
        try:
            customer = Customers.query.filter_by(id=customer_id).first()
            return jsonify(customer.serialize())

        except AttributeError as e:
            app.logger.error(str(e))
            return {"error": "Customer with id {} does not exist".format(customer_id)}, status.HTTP_404_NOT_FOUND

        except Exception as e:
            app.logger.error(str(e))
            return {"error": "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def put(self, customer_id):
        """
        put:
            summary: Update some or all fields of customer with given id.
            parameters:
                OPTIONAL: "first_name": <string>
                OPTIONAL: "last_name": <string>
                OPTIONAL: "phone_number": <string>
                OPTIONAL: "email": <string>
                OPTIONAL: "ssn": <string>
                OPTIONAL: "active": <bool>
            responses:
                200:
                    Returns JSON object of the customer that was updated.
                404:
                    Not Found: Customer with given array not found
                500:
                    Internal Server Error
        """
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

        except AttributeError as e:
            app.logger.error(str(e))
            return {"error": "Customer with id {} does not exist".format(customer_id)}, status.HTTP_404_NOT_FOUND

        except Exception as e:
            app.logger.error(str(e))
            return {"error": "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR


class AccountsIndexController(Resource):
    def get(self, customer_id):
        """
        get:
            summary: Return all accounts for given customer id.
            parameters:
            responses:
                200:
                    Returns array of JSON object accounts for given customer id.
                500:
                    Internal Server Error
        """
        try:
            accounts = db.session.query(Accounts).filter(Accounts.customer_id == customer_id).all()

            return jsonify([account.serialize() for account in accounts])

        except Exception as e:
            app.logger.error(str(e))
            return {"error": "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def post(self, customer_id):
        """
        post:
            summary: Create a new account for given customer.
            parameters:
                "account_type": <string>
                "balance": <float>
                "account_number": <string>
                "routing_number": <string>
                "status": <string>
                "active": <bool>
            responses:
                200:
                    Returns JSON object of the account that was created.
                400:
                    Bad Request: Most likely a param is missing
                500:
                    Internal Server Error
        """
        try:
            customer = Customers.query.filter_by(id=customer_id).first()

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

        except BadRequestKeyError as e:
            app.logger.error(str(e))
            return{"error": "Bad Request"}, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            app.logger.error(str(e))
            return {"error": "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR


class AccountsController(Resource):
    def get(self, customer_id, account_id):
        """
        get:
            summary: Show account for given customer id and account id.
            parameters:
            responses:
                200:
                    Returns JSON object of the account for given customer id and account id.
                404:
                    Not Found: Either customer id or account id not found
                500:
                    Internal Server Error
        """
        try:
            account = db.session.query(Accounts).filter(Accounts.customer_id == customer_id, Accounts.id == account_id).first()

            if not account:
                app.logger.error("Customer with id {} or account with id {} does not exist"
                                 .format(customer_id, account_id))

                return {"error": "Customer with id {} or account with id {} does not exist"
                        .format(customer_id, account_id)}, status.HTTP_404_NOT_FOUND

            return jsonify(account.serialize())

        except Exception as e:
            app.logger.error(str(e))
            return {"error": "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def put(self, customer_id, account_id):
        """
        put:
            summary: Update account with given account id.
            parameters:
                OPTIONAL: "account_type": <string>
                OPTIONAL: "balance": <float>
                OPTIONAL: "account_number": <string>
                OPTIONAL: "routing_number": <string>
                OPTIONAL: "status": <string>
                OPTIONAL: "active": <bool>
            responses:
                200:
                    Returns JSON object of the account that was updated.
                404:
                    Not Found: Account id or customer id not found.
                500:
                    Internal Server Error
        """

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

        except AttributeError as e:
            app.logger.error(str(e))
            return {"error": "Account with id {} or customer with id {} does not exist"
                    .format(account_id, customer_id)}, status.HTTP_404_NOT_FOUND

        except Exception as e:
            app.logger.error(str(e))
            return {"error": "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR


class LedgerController(Resource):
    def get(self, customer_id, account_id):
        """
        put:
            summary: Show all ledger info for an account.
            parameters:
            responses:
                200:
                    Returns array of JSON objects of the ledger info.
                404:
                    Not Found: Account id or customer id not found.
                500:
                    Internal Server Error
        """
        try:
            ledger = db.session.query(Accounts, Ledger).outerjoin(Ledger) \
                        .filter(Accounts.customer_id == customer_id) \
                        .filter(Ledger.account_id == account_id).all()

            # If ledger is an empty array it could be that there is no
            # ledger or it could be that the customer or account don't exist
            if not ledger:
                account = Accounts.query.filter_by(customer_id=customer_id, id=account_id).first()

                # If account doesn't exist you know either the customer or accounts
                # don't exist and can return an error
                if not account:
                    app.logger.error("Customer with id {} or account with id {} does not exist"
                                     .format(customer_id, account_id))

                    return {"error": "Customer with id {} or account with id {} does not exist"
                            .format(customer_id, account_id)}, status.HTTP_404_NOT_FOUND

                # Otherwise ledger is just empty
                else:
                    return jsonify([])

            return jsonify([l[1].serialize() for l in ledger])

        except Exception as e:
            app.logger.error(str(e))
            return {"error": "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR


class TransferController(Resource):
    def post(self, customer_id):
        """
        post:
            summary: Transfers money between accounts that the given user owns.
            parameters:
                "to_account_id": <int>
                "from_account_id": <int>
                "amount": <float>
            responses:
                200:
                    Returns JSON info about the transaction that took place.
                400:
                    Bad Request: Most likely a param is missing
                404:
                    Not Found: Account id or customer id not found.
                500:
                    Internal Server Error
        """
        try:
            to_account_id = request.values['to_account_id']
            from_account_id = request.values['from_account_id']
            amount = request.values['amount']

            if amount <= 0:
                return {"error": "Amount must be greater than 0"}, status.HTTP_400_BAD_REQUEST

            from_account = Accounts.query.filter_by(customer_id=customer_id, id=int(from_account_id)).first()

            if from_account.balance - float(amount) < 0:
                return {"error": "Insufficient in from account"}, status.HTTP_400_BAD_REQUEST

            to_account = Accounts.query.filter_by(customer_id=customer_id, id=int(to_account_id)).first()

            if not from_account.status == "opened" or not from_account.active \
                    or not to_account.status == "opened" or not to_account.active:

                return {"error": "Both to and from accounts must be open"}, status.HTTP_400_BAD_REQUEST

            to_account.balance = to_account.balance + float(amount)
            from_account.balance = from_account.balance - float(amount)

            object_array = [
                Ledger(
                    account_id=to_account_id,
                    account=to_account,
                    transaction_type="credit",
                    amount=amount,
                    details="transfer_in",
                ),
                Ledger(
                    account_id=from_account_id,
                    account=from_account,
                    transaction_type="debit",
                    amount=amount,
                    details="transfer_away",
                )
            ]

            db.session.bulk_save_objects(object_array)
            db.session.commit()

            return_json = {
                "to_account": to_account_id,
                "from_account": from_account_id,
                "amount": amount
            }

            return jsonify(return_json)

        except AttributeError as e:
            app.logger.error(str(e))
            return {"error": "Customer with id {} does not exist".format(customer_id)}, status.HTTP_404_NOT_FOUND

        except BadRequestKeyError as e:
            app.logger.error(str(e))
            return {"error": "Bad Request"}, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            app.logger.error(str(e))
            return {"error": "Internal Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR


# Routes
api.add_resource(CustomersIndexController, '/customers')
api.add_resource(CustomersController, '/customers/<string:customer_id>')
api.add_resource(AccountsIndexController, '/customers/<string:customer_id>/accounts')
api.add_resource(AccountsController, '/customers/<string:customer_id>/accounts/<string:account_id>')
api.add_resource(LedgerController, '/customers/<string:customer_id>/accounts/<string:account_id>/ledger')
api.add_resource(TransferController, '/customers/<string:customer_id>/transfer')

# Main app loop
if __name__ == '__main__':
    app.run()
