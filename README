# Technical Stack Used
Flask (micro python web framework), PostgreSQL, SQLAlchemy (Flask ORM for SQL Databases)

# Database Explination
I chose to use a SQL database primarily because of the major requirement of transfering
between two accounts and keeping a ledger. I wanted to make sure that my database was atomic
so that I could guarentee the transfer would not error half way through and money would get "lost".

# Structure of Project
app.py - This is the main logic of the api. Contains routes and controllers
models.py - Database models
config.py - Config file for flask
manage.py - Management script that runs the flask app
migrations/versions - Directory of database migrations. They are auto-generated but required some
					  manual changes.
