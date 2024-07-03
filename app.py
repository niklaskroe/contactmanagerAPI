from flask import Flask, url_for, request, render_template, abort, redirect, make_response, session, jsonify
from markupsafe import escape
from flask_mysqldb import MySQL
from itertools import chain

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'contact_db'

mysql = MySQL(app)

# Formatierung JSON
def contact_formatting(result):
    result_formatted = {
        "contact_id": result[0],
        "surname": result[1],
        "name": result[2],
        "number": result[3],
        "email": result[4]
    }
    return result_formatted

def folder_formatting(result):
    result_formatted = {
        "folderid": result[0],
        "name": result[1]
    }
    return result_formatted

# ------------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    return "Index"

# GET list of all contacts
@app.route('/contacts', methods=['GET'])
def get_all_contacts():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    results = cursor.fetchall()
    cursor.close()

    end_results = []

    for i in range(len(results)):
        result = results[i]
        result_formatted = contact_formatting(result)
        end_results.append(result_formatted)

    if results is None:
        abort(404)

    return jsonify(end_results)

# GET contact with id ...
@app.route('/contacts/<contact_id>', methods=['GET'])
def get_one_contact(contact_id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM contacts WHERE contactid = {contact_id}")
    result = cursor.fetchone()
    cursor.close()

    if result is None:
        abort(404)

    result_formatted = contact_formatting(result)

    return jsonify(result_formatted)

# GET folders in which contact with id ... is in
@app.route('/contacts/<contact_id>/folders', methods=['GET'])
def get_folders_where_contact(contact_id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT folder_folderid FROM folder_has_contact WHERE contact_contactid = {contact_id}")
    query = cursor.fetchall()

    values = tuple(chain.from_iterable(query))

    if len(values) == 1:
        value = values[0]
        cursor.execute(f"SELECT * FROM folders WHERE folderid = {value}")
    elif len(values) == 0:
        abort(404)
    else:
        cursor.execute(f"SELECT * FROM folders WHERE folderid IN {values}")

    
    results = cursor.fetchall()
    cursor.close()

    end_results = []

    for i in range(len(results)):
        result = results[i]
        result_formatted = folder_formatting(result)
        end_results.append(result_formatted)

    if result is None:
        abort(404)

    return jsonify(end_results)

# CREATE a new contact
@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()

    sql = (
        "INSERT INTO `contacts` (name, surname, number, email) "
        "VALUES (%s, %s, %s, %s)"
    )
    values = (data.get("surname"), data.get("name"), data.get("number"), data.get("email"))

    cursor = mysql.connection.cursor()
    cursor.execute(sql, values)

    mysql.connection.commit()
    cursor.close()

    return jsonify("")

# DELETE a contact
@app.route('/contacts/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id):            
    del_contact = (f"DELETE FROM contacts WHERE contactid = {contact_id}")

    cursor = mysql.connection.cursor()


    cursor.execute(f"SELECT contactid FROM contacts WHERE contactid = {contact_id}")
    result = cursor.fetchall()

    if result is None:
        abort(404)
    
    cursor.execute(del_contact)
    mysql.connection.commit()
    cursor.close()

    return jsonify("")

# ----------------------------------------------------------------

# GET all folders
@app.route('/folders', methods=['GET'])
def get_all_folders():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM folders')
    results = cursor.fetchall()
    cursor.close()

    end_results = []

    for i in range(len(results)):
        result = results[i]
        result_formatted = folder_formatting(result)
        end_results.append(result_formatted)

    if results is None:
        abort(404)

    return jsonify(end_results)

# GET details for folder with id ...
@app.route('/folders/<folder_id>', methods=['GET'])
def get_one_folder(folder_id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM folders WHERE folderid = {folder_id}")
    result = cursor.fetchone()
    cursor.close()

    if result is None:
        abort(404)

    result_formatted = folder_formatting(result)

    return jsonify(result_formatted)

# GET contacts from folder with id ...
@app.route('/folders/<folder_id>/contacts', methods=['GET'])
def get_contacts_in_folder(folder_id):
    cursor = mysql.connection.cursor()

    cursor.execute(f"SELECT contact_contactid FROM folder_has_contact WHERE folder_folderid = {folder_id}")
    contacts_in_folder = cursor.fetchall()
    cursor.close()

    values = tuple(chain.from_iterable(contacts_in_folder))

    cursor = mysql.connection.cursor()

    if len(values) == 1:
        value = values[0]
        cursor.execute(f"SELECT * FROM contacts WHERE contactid = {value}")
    elif len(values) == 0:
        abort(404)
    else:
        cursor.execute(f"SELECT * FROM contacts WHERE contactid IN {values}")

    
    results = cursor.fetchall()
    cursor.close()

    end_results = []

    for i in range(len(results)):
        result = results[i]
        result_formatted = contact_formatting(result)
        end_results.append(result_formatted)

    if result is None:
        abort(404)

    return jsonify(end_results)

# CREATE folder
@app.route('/folders', methods=['POST'])
def create_folder():
    data = request.get_json()
    values = data.get("name")
    
    sql = ("INSERT INTO `folders` (name) VALUES (%s)")
    
    cursor = mysql.connection.cursor()
    cursor.execute(sql, (values, ))
    mysql.connection.commit()
    cursor.close()

    return jsonify("")

# DELETE folder
@app.route('/folders/<folder_id>', methods=['DELETE'])
def delete_folder(folder_id):            
    del_folder = (f"DELETE FROM folders WHERE folderid = {folder_id}")

    cursor = mysql.connection.cursor()

    cursor.execute(f"SELECT folderid FROM folders WHERE folderid = {folder_id}")
    result = cursor.fetchall()

    if result is None:
        abort(404)

    cursor.execute(del_folder)
    mysql.connection.commit()
    cursor.close()

    return jsonify("")

# -------------------------------------------------------------

# CREATE folder contact relation
@app.route('/folders/<folder_id>/contacts', methods=['POST'])
def create_folder_contact_relation(folder_id):
    cursor = mysql.connection.cursor()
    data = request.get_json()
    contact_id = data.get("contactid")

    cursor.execute(f"INSERT INTO folder_has_contact VALUES ({folder_id}, {contact_id})")
    mysql.connection.commit()
    cursor.close()

    return jsonify("")

# DELETE folder contact relation
@app.route('/folders/<folder_id>/contacts/<contact_id>', methods=['DELETE'])
def delete_folder_contact_relation(folder_id, contact_id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"DELETE FROM folder_has_contact WHERE folder_folderid = {folder_id} AND contact_contactid = {contact_id}")
    mysql.connection.commit()
    cursor.close()

    return jsonify("")
