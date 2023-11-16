#!/usr/bin/perl

use strict;
use warnings;
use CGI;

# Create a new CGI object
my $cgi = CGI->new;

# Print the content type header
print $cgi->header('text/html');

# Get form data
my $name    = $cgi->param('name');
my $email   = $cgi->param('email');
my $gender  = $cgi->param('gender');
my $color   = $cgi->param('color');
my @interests = $cgi->param('interests');

# Print the HTML response
print <<HTML;
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Form Submission Result</title>
</head>
<body>
    <h2>Form Submission Result</h2>
    <p>Name: $name</p>
    <p>Email: $email</p>
    <p>Gender: $gender</p>
    <p>Favorite Color: $color</p>
    <p>Interests: @{[join(', ', @interests)]}</p>
</body>
</html>
HTML
