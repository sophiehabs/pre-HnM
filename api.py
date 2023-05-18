# -*- coding: utf-8 -*-
"""
api.ipynb
"""

#pip install flask-restx

from flask import Flask, jsonify
from sqlalchemy import create_engine
from flask_restx import Api, Namespace, Resource \

user = "root"
passw = "123456"
host = "34.132.212.141"
database = "main"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = host

api = Api(app, version = '1.0',
    title = 'The famous REST API with FLASK!',
    description = """
        This RESTS API is an API to built with FLASK
        and FLASK-RESTX libraries
        """,
    contact = "sophie.schaesberg@student.ie.edu",
    endpoint = "/api/v1"
)

def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

customers = Namespace('customers',
    description = 'All operations related to customers',
    path='/api/v1')
api.add_namespace(customers)

@customers.route("/customers")
class get_all_users(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM customer
            LIMIT 10;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@customers.route("/customers/<string:id>")
@customers.doc(params = {'id': 'The ID of the user'})
class select_user(Resource):

    @api.response(404, "CUSTOMER not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM customer
            WHERE customer_id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

if __name__ == '__main__':
    app.run(debug = True)