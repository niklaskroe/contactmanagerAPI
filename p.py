data = {
    "key": "value",
    "new": "new_val"
}

k, v = data.popitem()
new_data = v
data["id"] = "cid"

print(data, new_data)

# cursor = mysql.connection.cursor()

#     cursor.execute(f"SELECT contact_contactid FROM folder_has_contact WHERE folder_folderid = {folder_id}")
#     contacts_in_folder = cursor.fetchall()
#     cursor.close()

#     values = tuple(chain.from_iterable(contacts_in_folder))

#     cursor = mysql.connection.cursor()

#     if len(values) == 1:
#         value = values[0]
#         cursor.execute(f"SELECT * FROM contacts WHERE contactid = {value}")
#     elif len(values) == 0:
#         abort(404)
#     else:
#         cursor.execute(f"SELECT * FROM contacts WHERE contactid IN {values}")

    
#     results = cursor.fetchall()
#     cursor.close()

#     end_results = []

#     for i in range(len(results)):
#         result = results[i]
#         result_formatted = contact_formatting(result)
#         end_results.append(result_formatted)

#     if result is None:
#         abort(404)

#     return jsonify(end_results)

# EDIT existing contact
# @app.route('/contacts/<contact_id>', methods=['PUT'])
# def update_contact(contact_id):

#     cursor = mysql.connection.cursor()

#     cursor.execute(f"SELECT contactid FROM contacts WHERE contactid = {contact_id}")
#     result = cursor.fetchone()

#     if result is None:
#         abort(404)

#     data = request.get_json()
#     k, v = data.popitem()
#     folder_assignment = v
#     data["contact_id"] = contact_id
    
#     query = (f"SELECT * FROM folder_has_contact WHERE contact_contactid = {contact_id}")

#     sql = ("UPDATE contacts SET surname = %(surname)s, name = %(name)s, number = %(number)s, email = %(email)s WHERE contactid = %(contact_id)s")

#     new_assignment = (f"INSERT INTO folder_has_contact VALUES ({folder_assignment}, {contact_id})")
#     assignment = (f"UPDATE folder_has_contact SET folder_folderid = {folder_assignment} WHERE contact_contactid = {contact_id}")

#     cursor.execute(query)
#     query_result = cursor.fetchall()

#     if len(query_result) == 0:
#         cursor.execute(new_assignment)
#     else:
#         cursor.execute(assignment)

#     cursor.execute(sql, data)

#     mysql.connection.commit()

#     cursor.close()

#     return jsonify("")


# EDIT existing folder
# @app.route('/folders/<folder_id>', methods=['PUT'])
# def update_folder(folder_id):

#     cursor = mysql.connection.cursor()

#     cursor.execute(f"SELECT folderid FROM folders WHERE folderid = {folder_id}")
#     result = cursor.fetchone()

#     if result is None:
#         abort(404)

#     data = request.get_json()
#     data["folder_id"] = folder_id
    
#     sql = ("UPDATE folders SET name = %(name)s WHERE folderid = %(folder_id)s")

#     cursor.execute(sql, data)

#     mysql.connection.commit()

#     cursor.close()

#     return jsonify("")