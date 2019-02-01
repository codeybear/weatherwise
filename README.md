Folder Structure
================

The website is built using django, this library mostly dictates how the code is organised:

/schedule/models/
The models contains code mostly to handle talking to the database, as well as the reporting functions contained in weather.py.

/schedule/templates/
The templates render the HTML pages, each subfolder relates to a different page.
Each file in these sub folders relates to the particular view i.e. index.html is the list of items, detail.html is the item view.

/schedule/
The views* files in this folder take the incoming web request, call the relevant model and send the result to the relevant template.

/schedule/static/schedule/
This folder contains the static files.
This is just the location map, user guide and the front end JavaScript code.

Skills required
===============

Python

Django or a similar web development framework

Web development - HTML, CSS, JavaScript

SQL Databases (MYSQL preferred)

Non essentials:

Bootstrap to layout the forms and parsley.js to do form validation.  
pymysql is used to talk to MYSQL
