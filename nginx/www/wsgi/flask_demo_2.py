from flask import Flask, jsonify, request

app = Flask(__name__)

# Our data store
data_store = [
    {'id': '0', 'name': 'Jeff', 'email': 'jeff@jeff.com'},
    {'id': '1', 'name': 'Jeremy', 'email': 'jeremy@jeremy.com'},
]

# GET endpoint to retrieve data from the dictionary
@app.route('/api', methods=['GET'])

def get_data():
    return jsonify(data_store)

# POST endpoint to add new data to the dictionary
@app.route('/api', methods=['POST'])
def add_data():
    new_record = request.get_json()
    new_record['id'] = str(len(data_store))
    data_store.append(new_record)
    return new_record, 200

# add a method to delete records@app.route('/api', methods=['DELETE'])
@app.route('/api/<id>', methods=['DELETE'])
def remove_data(id):
    record_to_remove = next((record for record in data_store if record['id'] == id), None)
    if record_to_remove is not None:
        data_store.remove(record_to_remove)
        return '', 200
    else:
        return 'Record not found', 404

@app.route('/api', methods=['PATCH'])
def update_data():
    updated_record = request.get_json()
    id_to_update = updated_record.get('id')

    for record in data_store:
        if record['id'] == id_to_update:
            record.update(updated_record)
            return updated_record, 200

    return 'Record not found', 404
    
@app.route('/api/<id>', methods=['GET'])
def get_single_record(id):
    for record in data_store:
        if record['id'] == id:
            return jsonify(record), 200
    return 'Record not found', 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)