from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

app.config.from_object("config.ProductionConfig")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Customers, Accounts


@app.route("/")
def hello():
    return "Welcome to Tyler's Banking API"

# @app.route("/customers", methods=['POST', 'GET'])
# def customer():
#     name = request.args.get('name')
#     author = request.args.get('author')
#     published = request.args.get('published')
#     try:
#         customer = Customers(
#             name=name,
#             author=author,
#             published=published
#         )
#         db.session.add(customer)
#         db.session.commit()
#         return "Book added. book id={}".format(customer.id)
#     except Exception as e:
#         return(str(e))


@app.route("/getall")
def get_all():
    try:
        customer = Customers.query.all()

        return jsonify([a_customer.serialize() for a_customer in customer])

    except Exception as e:
        return(str(e))


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        customer = Customers.query.filter_by(id=id_).first()
        return jsonify(customer.serialize())
    except Exception as e:
        return(str(e))





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
    def get(self, _id):
        try:
            customer = Customers.query.filter_by(id=_id).first()
            return jsonify(customer.serialize())

        except Exception as e:
            return(str(e))

    def put(self, _id):
        try:
            customer = Customers.query.filter_by(id=_id).first()

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
    def get(self, _id):
        try:
            customer = Customers.query.filter_by(id=_id).first()
            accounts = Accounts.query.filter_by(customer=customer)

            return jsonify([account.serialize() for account in accounts])

        except Exception as e:
            return(str(e))

    def post(self, _id):
        customer = Customers.query.filter_by(id=_id).first()
        print customer
        try:
            print request.values['account_type']
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
            print "YO"
            db.session.add(account)
            db.session.commit()

            return jsonify(account.serialize())

        except Exception as e:
            return(str(e))

api.add_resource(CustomersIndexController, '/customers')
api.add_resource(CustomersController, '/customers/<string:_id>')
api.add_resource(AccountsIndexController, '/customers/<string:_id>/accounts')

if __name__ == '__main__':
    app.run()
