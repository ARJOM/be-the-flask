from flask import g, request, jsonify, abort

from app import app

from utils import generateUniqueId

from db.connection import get_db


# Ong

@app.route('/ongs', methods=['GET'])
def ongs_list():
    cur = get_db().cursor()
    cur.execute(f"SELECT * FROM ongs")
    ongs = cur.fetchone()
    cur.close()

    return jsonify(ongs)


@app.route('/ongs', methods=['POST'])
def ongs_new():
    if not request.json:
        abort(404)

    new = request.json
    id = generateUniqueId.generate_unique_id()

    cur = get_db().cursor()
    cur.execute(f"INSERT INTO ongs(id, name, email, whatsapp, city, uf) "
                f"VALUES ('{id}','{new['name']}','{new['email']}','{new['whatsapp']}','{new['city']}','{new['uf']}')")
    get_db().commit()
    cur.close()

    return jsonify({"id": id}), 201


@app.route('/sessions', methods=['post'])
def login():
    id = request.json["id"]

    cur = get_db().cursor()
    cur.execute(f"SELECT name FROM ongs WHERE id='{id}'")
    ong = cur.fetchone()
    cur.close()

    if ong is None:
        abort(404)

    return jsonify(ong)


# Incident

@app.route('/incidents', methods=['GET'])
def incidents_list():
    cur = get_db().cursor()
    cur.execute(f"SELECT i.*, o.name, o.email, o.whatsapp, o.city, o.uf FROM incidents i, ongs o WHERE i.ong_id=o.id")
    incidents = cur.fetchall()
    cur.close()

    return jsonify(incidents)


@app.route('/incidents', methods=['post'])
def incidents_new():
    if not request.json:
        abort(404)

    ong_id = request.headers['authorization']
    new = request.json

    cur = get_db().cursor()

    cur.execute(f"SELECT * FROM ongs WHERE id='{ong_id}'")
    ong = cur.fetchone()
    if ong is None:
        abort(404)

    cur.execute(f"INSERT INTO incidents(title, description, value, ong_id) "
                f"VALUES ('{new['title']}','{new['description']}',{new['value']},'{ong_id}')")
    get_db().commit()
    cur.close()

    return {}, 201


@app.route('/incidents/<int:incident_pk>', methods=['GET'])
def incidents_detail(incident_pk):
    cur = get_db().cursor()
    cur.execute(f"SELECT * FROM incidents WHERE id={incident_pk}")
    incident = cur.fetchone()
    cur.close()

    if incident is None:
        abort(404)

    return jsonify(incident)


@app.route('/incidents/<int:incident_pk>', methods=['DELETE'])
def incidents_delete(incident_pk):
    ong_id = request.headers['authorization']

    cur = get_db().cursor()
    cur.execute(f"SELECT ong_id FROM incidents WHERE id={incident_pk}")
    incident = cur.fetchone()

    if incident is None:
        abort(404)

    if incident['ong_id'] != ong_id:
        abort(401)

    # Deleting
    cur.execute(f"DELETE FROM incidents WHERE id={incident_pk} AND ong_id='{ong_id}'")
    get_db().commit()
    cur.close()

    return jsonify({'result': True})


# Profile

@app.route('/profile', methods=['GET'])
def profile():
    ong_id = request.headers['authorization']

    cur = get_db().cursor()
    cur.execute(f"SELECT * FROM incidents WHERE ong_id='{ong_id}'")
    incidents = cur.fetchall()

    return jsonify(incidents)
