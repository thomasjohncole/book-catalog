# Book Catalog 2018 #

The Book Catalog 2018 is a web application which displays information about various books by performing SQL queries and displaying the results in a user-friendly format. Information such as author, title, category, and a brief description are displayed in the browser.

This is a CRUD (Create, Read, Update, Delete) application built with the Flask web framework using Python.

SQLite is used as the database, and SQLAlchemy is utilized as the ORM.

The project was built inside an Ubuntu 16 virtual machine using Virtualbox and Vagrant.

In addition to the applications and extensions included in the Vagrantfile, flask-bootstrap was also installed manually, to facilitate CSS styling.

The application allows for user login using the Google OAuth method. Once logged in, users can add their own books and categories to the database, which will be displayed by the application.

## Files included ##

* catalog.py - the main Flask application file
* dbsetup.py - this file creates the database schema using SQLAlchemy
* populator.py - this file will add initial information to the database tables
* books.db - the actual SQLite database
* client_secrets.json - this file contains information used by Google OAuth
* book-catalog.sublime-workspace - this is a file used by the Sublime text editor, it's not needed to run the application and it's only useful if you're using Sublime.
* various templates - these are the Jinja templates which are used for the HTML views seen by the user, found in the Templates directory

## How to Make It Work ##

1. Install VirtualBox, Vagrant, and Git on the operating system of your choice.

2. Clone the Udacity repository which contains the Vagrantfile by running the command:`git clone https://github.com/udacity/fullstack-nanodegree-vm`

3. Install and/or boot the virtual machine from within the fullstack-nanodegree-vm/vagrant directory by running the command: `vagrant up`

4. Clone this repository in the fullstack-nanodegree/vagrant/catalog directory by running the command: `git clone https://github.com/colecode-ph/book-catalog.git .` (make sure the catalog directory is empty, or this command will fail.)

5. Connect to the virtual machine shell using the command: `vagrant ssh`

6. Install flask-bootstrap in the virtual machine using the command: `pip install flask-bootstrap`

7. Use the Google Developer's Console (https://console.developers.google.com) to generate a Client ID and Client Secret for a new web application called libro-catalog. (If you need to use a different name for the application, make sure to change the APPLICATION_NAME variable in line 32 of the catalog.py file)

8. Assign these generated values to the OS environment variables GOOGLE_CLIENT_SECRET, and GOOGLE_CLIENT_ID, respectively.

9. Change directories into the application directory (/vagrant/catalog).

10. Delete the existing database file with the command `rm books.db`

11. Run the shell command: `python db_setup.py` to create the database.

12. Run the shell command: `python populator.py` to add the data to the database.

13. Run the shell command: `python catalog.py` to start the application.

14. Open your browser to http://localhost:5000

15. Also hosted on an AWS Lightsail server at http://13.250.103.155.nip.io/



