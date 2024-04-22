import logging
from os import environ
from flask import Flask
from flask_pymysql import MySQL

logging.basicConfig(level=10, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

connect_args = {
    'user': environ['MYSQL_USERNAME'],
    'password': environ['MYSQL_PASSWORD'],
    'host': environ['MYSQL_HOST'],
    'port': int(environ['MYSQL_PORT']),
    'autocommit': True,
    'cursorclass': 'DictCursor'
}

app.config['pymysql_kwargs'] = connect_args

mysql = MySQL(app)


@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return str(rv)


if __name__ == '__main__':
    app.run(debug=True)
