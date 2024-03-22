#! /usr/bin/env python3
#
#
import sys
from datetime import datetime as dt

from flask import Flask, render_template, request, jsonify, make_response

# from flask_debugtoolbar import DebugToolbarExtension      I really want to do this, but I do not want to take
# troubleshooting time for the debugging tool bar now

LOGFILENAME = "flask_log_"
app = Flask(__name__)

# Sample data
items = {}


@app.route('/')
def make_form():
    print("In make_form", file=sys.stderr)
    log_something("Created the HTML file")
    return html, 200  # Variable html is defined before call app.run, below.
    # I did that to make this method easy to understand


# API endpoint for listing items
@app.route('/api/items', methods=['GET'])
def get_items():
    print("In get_items", file=sys.stderr)
    r = make_response((items, 200, {"Content-Type": "application/json"}))
    return r


# API endpoint for creating an item
@app.route('/api/items', methods=['POST'])
def create_item():
    """
    There is a flaw here: POST is supposed to create a new item.  In this implementation, if items[key] already exists,
    then create_item should return an error.  It doesn't, it overwrites items[key]  Fix this.
    :return:
    """
    print("In create_item", file=sys.stderr)
    # request.form returns parsed form data from a PUT or POST operation
    data = request.form
    # I think something is wrong with the way I am calling nginx using httpx.  Using the form works.
    # Both
    # httpx -v -m POST -d key key_7000 -d value value_7000 -h Content-Type application/json http://e7240/api/items
    # and
    # httpx -v -m POST -p key key_7000 -p value value_7000 -h Content-Type application/json http://e7240/api/items
    # Cause a failure.
    if data.get(key='key', default=None) is None:
        data = request.args  # POST should not put arguments in the URL
        if data.get(key='key', default=None) is None:
            return "Can't find the arguments.  " \
                   "This might be a problem with the client, might be a problem with the server", 500
        else:
            print(f"Got the arguments from the URL after all (was expecting from a form).")
    # data is a werkzeug.datastructures.structures.ImmutableMultiDict which is an immutable MultiDict.
    print(f"the keys in data are {data.keys()},\n data is {data}\n", file=sys.stderr)
    sys.stderr.flush()

    key = data.get(key='key', default=None)
    value = data.get(key='value', default=None)
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
@app.route('/api/items/', methods=['PUT'])
def update_item():
    """Update a value in the items dictionary"""
    print("In update_item", file=sys.stderr)
    data = request.form
    # I ought to put in some code here to attempt to pick up a value for key from the URL - that's a user error.
    # This should be a function instead of copy and pasting in the source code
    if data.get(key='key', default=None) is None:
        log_something("The key was not in the form or something else went wrong.  Trying to get from the URL")
        data = request.args  # PUT should not put arguments in the URL
        if data.get(key='key', default=None) is None:
            log_something("The key was not in the URL (and should not have been) or something else went wrong." 
                          "Giving up")
            return "Can't find the arguments.  " \
                   "This might be a problem with the client, might be a problem with the server", 500
        else:
            print(f"Got the arguments from the URL after all (was expecting from a form).")
    # This can be moved into the conditional - DRY
    key = data.get(key='key')
    value = data.get(key='value')
    log_something(f"In update_item: The key is {key} and the value is {value}")
    # Should check that key is not already in items.  If it is not, then technically, it should indicate that and let
    # higher level software deal with it.
    items[key] = value
    r = make_response((f"Successfully removed {key}", 204, {"Content-Type": "text/text"}))
    return r


# API endpoint for deleting an item
@app.route('/api/items/', methods=['DELETE'])
def delete_item():
    print("In delete_item", file=sys.stderr)
    """This should handle the case where items[key] is already gone"""
    data = request.args
    key = data.get(key='key', default=None)
    log_something(f"In delete_item.  key is {key}")
    if key is None:
        r = make_response(("A value for key was not found.  Something is wrong", 400, {"Content-Type": "text/text"}))
    else:
        if key in items:
            del items[key]
            r = make_response((f"Successfully removed {key}", 204, {"Content-Type": "text/text"}))
        else:
            r = make_response((f"{key} was found in the dictionary", 410, {"Content-Type": "text/text"}))
    return r


def log_something(msg: str):
    # I could use the standard python logger, but that's too complicated for what I want to do.  I just want a simple
    # file with messages as appropriate and with a timestamp.
    global logfile
    now_ = dt.now()
    now_str_ = now_.isoformat()
    print(f"{now_str_} {msg} ", file=sys.stderr)
    print(f"{now_str_} {msg} ", file=logfile)
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
    logfilename = LOGFILENAME + ".txt"
    logfile = open(logfilename, "a+")
    print(f"Server starting: logfilename  is {logfilename} ", file=sys.stderr)
    log_something("****** Server starting ************")
    app.run(debug=True)
