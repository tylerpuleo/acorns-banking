"""
Author: Tyler Puleo
License: GPL
Version: 0.0.1
Maintainer: Tyler Puleo
Status: Production
Summary: This is a small testing file that I used to test the post requests
         for my api. I tested the PUT requests with Postman and the GET requests
         with the browser.
"""

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
    "account_number": "12345678905",
    "routing_number": "987654321",
    "status": "opened",
    "active": True

}

transfer = {
    "to_account_id": 7,
    "from_account_id": 8,
    "amount": 9.99
}

response = requests.post('http://127.0.0.1:5000/customers', data=customer, verify=False)
response = requests.post('http://127.0.0.1:5000/customers/1/accounts', data=account, verify=False)
response = requests.post('http://127.0.0.1:5000/customers/1/transfer', data=transfer, verify=False)

print response

print response.text
