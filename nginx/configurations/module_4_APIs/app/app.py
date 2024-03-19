from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample data
items = []


@app.route('/')
def index():
    return html, 200  # html is defined just before call app.run, below.  I did that to make this method easy to understand


# API endpoint for listing items
@app.route('/api/items', methods=['GET'])
def get_items():
    # jsonify, a.k.a. flask.json.jsonify  returns a Response object with MIME type application/json
    return jsonify(items)


# API endpoint for creating an item
@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.json
    items.append(data)
    return jsonify(data), 201  # This must be 201 (Created) and not 200


# API endpoint for updating an item
@app.route('/api/items/<int:index>', methods=['PUT'])
def update_item(index):
    data = request.json
    items[index] = data
    return jsonify(data)


# API endpoint for deleting an item
@app.route('/api/items/<int:index>', methods=['DELETE'])
def delete_item(index):
    del items[index]
    return jsonify({'message': 'Item deleted'}), 200


if __name__ == '__main__':
    action = "/api/items"
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>REST Test</title>
    </head>
    <body>
        <h1>REST Test</h1>
        <!-- is a location within the virtual server which makes the connection to the flask middleware -->
        <!-- Add a form for GET -->
        <form action="{action}" method="POST">
            <label for="key">Key:</label>
            <input type="text" id="key" name="key" required><br>
            <label for="value">Value:</label>
            <input type="text" id="value" name="value" required><br>
            <button type="submit">POST</button>
        </form>
        <br>
        <form action="{action}" method="PUT">
            <label for="key_put">Key:</label>
            <input type="text" id="key_put" name="key" required><br>
            <label for="value_put">Value:</label>
            <input type="text" id="value_put" name="value" required><br>
            <button type="submit">PUT</button>
        </form>
        <br>
        <form action="{action}" method="DELETE">
            <label for="key_delete">Key:</label>
            <input type="text" id="key_delete" name="key" required><br>
            <button type="submit">DELETE</button>
        </form>
        <br>
    </body>    

        """
    app.run(debug=True)
