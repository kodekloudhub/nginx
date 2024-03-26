from flask import Flask, request, render_template

app = Flask(__name__)

# Sample data
data = {}


@app.route('/', methods=['GET'])
def get_data():
    return str(data)


@app.route('/', methods=['POST'])
def add_data():
    key = request.args.get('key')
    value = request.args.get('value')
    if key and value:
        data[key] = value
        return "Added successfully"
    else:
        return "Invalid input"


@app.route('/', methods=['PUT'])
def update_data():
    key = request.args.get('key')
    value = request.args.get('value')
    if key in data:
        data[key] = value
        return "Updated successfully"
    else:
        return "Key does not exist"


@app.route('/', methods=['DELETE'])
def delete_data():
    key = request.args.get('key')
    if key in data:
        del data[key]
        return "Deleted successfully"
    else:
        return "Key does not exist"


@app.route('/test', methods=['GET'])
def test_page():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)

