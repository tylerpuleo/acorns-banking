import requests
import datetime
import json

customer = {
    "first_name": "Tyler",
    "last_name": "Puleo",
    "phone_number": "978-995-6042",
    "email": "tyler@tyler.com",
    "ssn": "123-45-6789",
    "active": True

}

account = {
    "account_type": "checking",
    "balance": 150.00,
    "account_number": "1234567890",
    "routing_number": "987654321",
    "status": "opened",
    "active": True

}

transfer = {
    "to_account_id": 7,
    "from_account_id": 4,
    "amount": 9.99
}

# response = requests.post('http://127.0.0.1:5000/customers', data=customer, verify=False)
# response = requests.post('http://127.0.0.1:5000/customers/1/accounts', data=account, verify=False)
response = requests.post('http://127.0.0.1:5000/customers/1/transfer', data=transfer, verify=False)

print response

print response.text
