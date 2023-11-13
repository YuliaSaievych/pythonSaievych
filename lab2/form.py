#!/usr/bin/env python
use strict;
use warnings FATAL => 'all';
import cgi

# Enable debugging to catch errors in the browser
cgi.cgitb.enable()

# Get form data
form = cgi.FieldStorage()

# Set the content type to HTML
print("Content-type: text/html\n")

# Start HTML document
print("<html>")
print("<head>")
print("<title>CGI Form Processing</title>")
print("</head>")
print("<body>")

# Print the received form data
print("<h2>Form Data Received:</h2>")
print("<ul>")
for field in form.keys():
    print("<li><strong>{}</strong>: {}</li>".format(field, form[field].value))
print("</ul>")

# End HTML document
print("</body>")
print("</html>")

