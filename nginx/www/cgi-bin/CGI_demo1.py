#!/usr/bin/env python3

# Import necessary CGI modules
import cgi
import cgitb

# Enable debugging
cgitb.enable()

# Print necessary headers
print("Content-Type: text/html")
print()

# Read form data
form = cgi.FieldStorage()

# Get the value of the input field named 'name'
name = form.getvalue('name')

# Start HTML content
print("<html>")
print("<head>")
print("<title>CGI Example</title>")
print("</head>")
print("<body>")

# Process form data and display response
if name:
    print("<h1>Hello, {}!</h1>".format(name))
else:
    print("<h1>Hello, anonymous!</h1>")

print("<form method='post' action='example_cgi.py'>")
print("<label for='name'>Enter your name:</label>")
print("<input type='text' id='name' name='name'>")
print("<input type='submit' value='Submit'>")
print("</form>")

print("</body>")
print("</html>")

