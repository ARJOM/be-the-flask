import psycopg2

from flask import g

from app import app

# ~~~~
@app.before_request
def before_request():
    g.db = psycopg2.connect('dbname=bethehero user=flask password=flask host=127.0.0.1')


@app.teardown_request
def teardown_request(exception):
    g.db.close()
# ~~~~


@app.route('/ongs', methods=['GET'])
def ongs_list(request):
    data = {}
    data['ongs'] =
    return data