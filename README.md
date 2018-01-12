# Book Catalog 2018
## Project 4 in the Full Stack Web Developer Nanodegree

The Book Catalog 2018 is a web application which displays information about various books by performing various SQL queries and displaying the results in a user-friendly format. Information such as author, title, category, and a breif description are displayed in the browser.

This is a CRUD (Create, Read, Update, Delete) application built with the Flask web framework using Python.

SQLite is used as the database, and SQLAlchemy is utilized as the ORM.

The project was built inside an Ubuntu 16 virtual machine using Virtualbox and Vagrant.

In addition to the applications and extensions included in the Vagrantfile, flask-bootstrap was also installed manually, to facilitate CSS styling

The application allows for user login using the Google OAuth method. Once logged in , users can add their own books and categories to the database, which will be displayed by the application.

## Files included

catalog.py - the main Flask application file
dbsetup.py - this file creates the database schema using SQLAlchemy
populator.py - this file will add initial information to the database tables
books.db - the actual SQLite database
client_secrets.json - this file contains information used by Google OAuth
book-catalog.sublime-workspace - this is a file used by the Sublime text editor
various templates - these are the Jinja templates which are used for the HTML views seen by the user, found in the templates directory

## How to Make It Work

Install the virtual machine using Vagrant using the instructions found here:

Install flask-bootstrap in the vm using the command: pip install flask-bootstrap

Use your Google Developer credentials to generate a client_id and client_secret for the application. Then assign these values to the environment variables GOOGLE_CLIENT_SECRET, and GOOGLE_CLIENT_ID, respectively.

Clone the repository to the home directory of your virtual machine.

CD into the application directory.

Run the shell command python db_setup.py to create the database.

Run the shell command python populator.py to add the data to the database.

Run the shell command python catalog.py to start the application.

Open your browser to http://localhost:5000

Enjoy! Thanks for reviewing this project!

 

