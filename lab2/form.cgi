#!/usr/bin/env python

import cgi
import http.cookies as Cookies

# Enable debugging to catch errors in the browser
cgi.cgitb.enable()

# Get form data
form = cgi.FieldStorage()

# Set the content type to HTML
print("Content-type: text/html")

# Create a cookie to store the submission count
submission_count_cookie = Cookies.SimpleCookie()

# Get the current count from the cookie
submission_count = int(form.getfirst("submission_count", 0))
submission_count += 1

# Set the new count in the cookie
submission_count_cookie["submission_count"] = str(submission_count)

# Print the cookie header
print(submission_count_cookie.output())

# Start HTML document
print("\n<html>")
print("<head>")
print("<title>CGI Form Processing with Cookies</title>")
print("</head>")
print("<body>")

# Print the received form data
print("<h2>Form Data Received:</h2>")
print("<ul>")
for field in form.keys():
    print("<li><strong>{}</strong>: {}</li>".format(field, form[field].value))
print("</ul>")

# Display submission count from the cookie
print("<h2>Submission Count:</h2>")
print("<p>This form has been submitted {} times.</p>".format(submission_count))

# Button to clear all cookies
print('<form method="post" action="{}">'.format(form.getfirst("SCRIPT_NAME", "")))
print('<input type="hidden" name="clear_cookies" value="true">')
print('<input type="submit" value="Clear Cookies">')
print('</form>')

# End HTML document
print("</body>")
print("</html>")
