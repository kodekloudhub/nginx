#! /usr/bin/env python3
#
#
import sys
from datetime import datetime as dt

from flask import Flask, render_template, request, jsonify, make_response
from flask_debugtoolbar import DebugToolbarExtension

LOGFILENAME = "flask_log_"
app = Flask(__name__)

# Sample data
items = {}


@app.route('/')
def index():
    log_something("Created the HTML file")
    return html, 200  # Variable html is defined before call app.run, below.
    # I did that to make this method easy to understand


# API endpoint for listing items
@app.route('/api/items', methods=['GET'])
def get_items():
    r = make_response((items, 200, {"Content-Type": "application/json"}))
    return r


# API endpoint for creating an item
@app.route('/api/items', methods=['POST'])
def create_item():
    # request.form returns parsed form data from a PUT or POST operation
    data = request.form
    # I think something is wrong with the way I am calling nginx using httpx.  Using the form works.
    # Both
    # httpx -v -m POST -d key key_7000 -d value value_7000 -h Content-Type application/json http://e7240/api/items
    # and
    # httpx -v -m POST -p key key_7000 -p value value_7000 -h Content-Type application/json http://e7240/api/items
    # Cause a failure.
    if data.get(key='key', default=None) is None:
        data = request.args     # POST should not put arguments in the URL
        if data.get(key='key', default=None) is None:
            return "Can't find the arguments.  " \
                "This might be a problem with the client, might be a problem with the server", 500
        else:
            print(f"Got the arguments from the URL after all")
    # data is a werkzeug.datastructures.structures.ImmutableMultiDict which is an immutable MultiDict.
    print(f"the keys in data are {data.keys()},\n data is {data}\n", file=sys.stderr)
    sys.stderr.flush()

    key = data.get(key='key', default=None)
    value = data.get(key='key', default=None)
    if key is None or value is None:
        return f"Having troubles decoding the query.  key is {key} and value is {value}", 500

    print(f"Value for key is {key} and value is: {value}")
    items[key] = value
    log_something(f"in create_item:  data is {data}  data.keys() is {data.keys()}, items is now {items}.")
    # status must be 201 (Created) and not 200 (Okay)
    # See https://tedboy.github.io/flask/interface_api.application_object.html?highlight=make_response#flask.Flask.make_response    # noqa
    r = make_response((items, 201, {"Content-Type": "application/json"}))
    return r


# API endpoint for updating an item
@app.route('/api/items/<int:index>', methods=['PUT'])
def update_item(index):
    data = request.json
    log_something(f"in update_item.  Data is {data} items is now {items}.")
    items[index] = data
    return jsonify(data)


# API endpoint for deleting an item
@app.route('/api/items/<int:index>', methods=['DELETE'])
def delete_item(index):
    log_something(f"In delete_item.  Index is {index}")
    del items[index]
    return jsonify({'message': 'Item deleted'}), 200


def log_something(msg: str):
    # I could use the standard python logger, but that's too complicated for what I want to do.  I just want a simple
    # file with messages as appropriate and with a timestamp.
    global logfile
    now = dt.now()
    now_str = now.isoformat()

    print(f"{now_str} {msg} ", file=logfile)
    logfile.flush()


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
    now = dt.now()
    now_str = now.isoformat()
    # filename = LOGFILENAME + now_str + ".txt"
    filename = LOGFILENAME + ".txt"
    logfile = open(filename, "a+")
    print(f"To stderr: logfilename  is {filename} ", file=sys.stderr)
    log_something("****** Server starting ************")
    app.run(debug=True)
