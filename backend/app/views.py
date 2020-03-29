import psycopg2
import psycopg2.extras
from flask import g, request, jsonify, abort

from app import app

from utils import generateUniqueId

# ~~~~
@app.before_request
def before_request():
    g.db = psycopg2.connect('dbname=bethehero user=flask password=flask host=127.0.0.1')


@app.teardown_request
def teardown_request(exception):
    g.db.close()
# ~~~~


@app.route('/ongs', methods=['GET'])
def ongs_list():
    data = {}
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT * FROM ongs")
    data['ongs'] = cur.fetchall()
    cur.close()
    return data


@app.route('/ongs', methods=['POST'])
def ongs_new():
    if not request.json:
        abort(404)
    new = request.json
    id = generateUniqueId.generate_unique_id()
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"INSERT INTO ongs(id, name, email, whatsapp, city, uf) "
                f"VALUES ('{id}','{new['name']}','{new['email']}','{new['whatsapp']}','{new['city']}','{new['uf']}')")
    g.db.commit()
    cur.close()
    return jsonify({'task': request.json}), 201
