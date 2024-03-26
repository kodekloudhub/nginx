from wsgiref.simple_server import make_server

import hashlib

# Define the filename for storing username-password pairs
PASSWORD_FILE = "passwords.txt"


def load_passwords():
    passwords_ = {}
    try:
        with open(PASSWORD_FILE, "r") as file:
            for line in file:
                username, password_hash = line.strip().split(":")
                passwords_[username] = password_hash
    except FileNotFoundError:
        pass
    return passwords_


def save_passwords(passwords_):
    with open(PASSWORD_FILE, "w") as file:
        for username, password_hash in passwords_.items():
            file.write(f"{username}:{password_hash}\n")


def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    if environ['REQUEST_METHOD'] == 'POST':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            content_length = 0

        request_body = environ['wsgi.input'].read(content_length).decode()
        params = dict(x.split('=') for x in request_body.split('&'))

        if 'action' in params:
            if params['action'] == 'add':
                if 'username' in params and 'password' in params:
                    username = params['username']
                    password = params['password']
                    passwords[username] = hashlib.sha256(password.encode()).hexdigest()
                    save_passwords(passwords)
                    response = "User added successfully."
                else:
                    response = "Both username and password are required."
            elif params['action'] == 'remove':
                if 'username' in params:
                    username = params['username']
                    if username in passwords:
                        del passwords[username]
                        save_passwords(passwords)
                        response = "User removed successfully."
                    else:
                        response = "User not found."
                else:
                    response = "Username is required."
            elif params['action'] == 'change':
                if 'username' in params and 'password' in params:
                    username = params['username']
                    password = params['password']
                    if username in passwords:
                        passwords[username] = hashlib.sha256(password.encode()).hexdigest()
                        save_passwords(passwords)
                        response = "Password changed successfully."
                    else:
                        response = "User not found."
                else:
                    response = "Both username and password are required."
            else:
                response = "Invalid action."
        else:
            response = "Action parameter is missing."
    else:
        response = "Invalid request method."

    start_response(status, headers)
    return [response.encode()]


if __name__ == '__main__':
    passwords = load_passwords()
    with make_server('', 8000, application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()

