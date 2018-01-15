import httplib2
import json
import os
import random
import requests
import string

from db_setup import Base, Category, Book, User

from flask import (
    Flask, request, render_template, redirect,
    url_for, flash, jsonify, make_response
    )
from flask import session as login_session
from flask_bootstrap import Bootstrap

from oauth2client.client import (
    flow_from_clientsecrets, OAuth2WebServerFlow, FlowExchangeError
    )

from sqlalchemy import create_engine, func, update
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
Bootstrap(app)

# you MUST REGISTER this app with Google before this will do anything!
# get will return None if key doesn't exist
CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
gclient_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
APPLICATION_NAME = "libro-catalog"

engine = create_engine('sqlite:///books.db')
# binds the engine to the Base class
Base.metadata.bind = engine
# makes the connections between class definitions & corresponding tables in db
DBSession = sessionmaker(bind=engine)
# creates sessionmaker object, which establishes link of
# communication between our code executions and the engine we created
session = DBSession()
# creates an instance of the DBSession  object - to make a changes
# to the database, we can call a method within the session


# index page views and corresponding JSON enpoint functions
@app.route('/')
def indexPage():
    """ Shows a list of categories and a list of books, sorted by title """
    books = session.query(Book).order_by(Book.title)
    category_counts = (
        session.query(Category.name, Category.id,
                      func.count(Book.title).label("count")
                      )
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )
    if 'username' not in login_session:
        return render_template('index_public.html',
                               category_counts=category_counts, books=books)
    else:
        user = login_session['email']
        return render_template('index.html', books=books,
                               category_counts=category_counts, user=user)


@app.route('/JSON')
def indexPageJSON():
    """ creates a JSON endpoint for the indexPage view function """
    books = session.query(Book).order_by(Book.title)
    category_counts = (
        session.query(Category.name, Category.id,
                      func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )
    # define empty list for the categories with title counts
    cat_counts = []
    # iterate through query results and create dictionary
    for category in category_counts:
        for book in books:
            result = {
                'Category Name': category.name,
                'Title Count': category.count,
            }
        # append dictionary to list, creating a list of dictionaries
        cat_counts.append(result)

    # define empty list for book  titles with category name and author
    book_list = []
    # iterate through results and create dictionary
    for book in books:
        for category in category_counts:
            if category.id == book.category_id:
                # this will assign the proper category name to the book
                result = {
                    'Title': book.title,
                    'Author': book.author,
                    'Category': category.name,
                }
        # append dictionary to list, creating a list of dictionaries
        book_list.append(result)
    # use jsonify to format the two lists for the JSON endpoint
    return jsonify(Categories=cat_counts, Books=book_list)


@app.route('/author-sorted')
def indexAuthorSorted():
    """ Shows a list of categories and a list of books, sorted by author """
    books = session.query(Book).order_by(Book.author)
    category_counts = (
        session.query(Category.name, Category.id,
                      func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )
    if 'username' not in login_session:
        return render_template('index_public.html', books=books,
                               category_counts=category_counts)
    else:
        user = login_session['email']
        return render_template('index.html', books=books,
                               category_counts=category_counts, user=user)


@app.route('/author-sorted/JSON')
def indexAuthorSortedJSON():
    """ creates a JSON endpoint for the indexAuthorSorted view function """
    books = session.query(Book).order_by(Book.author)
    category_counts = (
        session.query(Category.name, Category.id,
                      func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )
    # define empty list for the categories with title counts
    cat_counts = []
    # iterate through query results and create dictionary
    for category in category_counts:
        result = {
            'Category Name': category.name,
            'Title Count': category.count,
        }
        # append dictionary to list, creating a list of dictionaries
        cat_counts.append(result)

    # define empty list for books with category and author
    book_list = []
    # iterate through results and create dictionary
    for book in books:
        for category in category_counts:
            if category.id == book.category_id:
                # this will assign the proper category name to the book
                result = {
                    'Title': book.title,
                    'Author': book.author,
                    'Category': category.name,
                }
        # append dictionary to list, creating a list of dictionaries
        book_list.append(result)
    # use jsonify to format the two lists for the JSON endpoint
    return jsonify(Categories=cat_counts, Books=book_list)


@app.route('/category-sorted')
def indexCategorySorted():
    """ Shows a list of categories and a list of books, sorted by category """
    books = (
        session.query(Book.title, Book.author, Book.id, Book.category_id,
                      Category.id, Category.name)
        .join(Category, Book.category_id == Category.id)
        .order_by(Category.name)
        )

    category_counts = (
        session.query(Category.name, Category.id,
                      func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )
    if 'username' not in login_session:
        return render_template('index_public.html', books=books,
                               category_counts=category_counts)
    else:
        user = login_session['email']
        return render_template('index.html', books=books,
                               category_counts=category_counts, user=user)


@app.route('/category-sorted/JSON')
def indexCategorySortedJSON():
    """ creates a JSON endpoint for the indexCategorySorted view function """
    books = (
        session.query(Book.title, Book.author, Book.id, Book.category_id,
                      Category.id, Category.name)
        .join(Category, Book.category_id == Category.id)
        .order_by(Category.name)
        )

    category_counts = (
        session.query(Category.name, Category.id,
                      func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )
    # define empty list for the categories with title counts
    cat_counts = []
    # iterate through query results and create dictionary
    for category in category_counts:
        result = {
            'Category Name': category.name,
            'Title Count': category.count,
        }
        # append dictionary to list, creating a list of dictionaries
        cat_counts.append(result)
    # define empty list for books with category and author
    book_list = []
    # iterate through results and create dictionary
    for book in books:
        for category in category_counts:
            if category.id == book.category_id:
                # this will assign the proper category name to the book
                result = {
                    'Title': book.title,
                    'Author': book.author,
                    'Category': category.name,
                }
        # append dictionary to list, creating a list of dictionaries
        book_list.append(result)
    # use jsonify to format the two lists for the JSON endpoint
    return jsonify(Categories=cat_counts, Books=book_list)


# category create, update, and delete functions
@app.route('/categories/create', methods=['GET', 'POST'])
def createCategory():
    """ Create a new category """
    if 'username' not in login_session:
        return redirect('/login')

    category_counts = (
        session.query(Category.name, Category.id,
                      func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )

    if request.method == 'POST':
        new_category = Category(name=request.form['category_name'])

        if not request.form['category_name']:
            flash('You must fill out the form! Duh!')
            return redirect(url_for('createCategory'))

        for category in category_counts:
            if request.form['category_name'] == category.name:
                flash('''The category name: {} - is already in use.
                      Duplicate names are not allowed.'''
                      .format(category.name))
                return redirect(url_for('createCategory'))

        session.add(new_category)
        session.commit()
        flash("Category: {} created successfully!".format(new_category.name))
        return redirect(url_for('indexPage'))
    else:
        user = login_session['email']
        return render_template('create_category.html',
                               category_counts=category_counts, user=user)


@app.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    """ Edit the name of an existing category """
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(id=category_id).one()
    category_counts = (
        session.query(Category.name, Category.id,
                      func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )

    if request.method == "POST":
        data = ({"name": request.form["category_name"]})

        if not request.form["category_name"]:
            flash('Form field cannot be blank!')
            return redirect(url_for('editCategory', category_id=category_id))

        session.query(Category).filter_by(id=category_id).update(data)
        session.commit()
        flash("Category: {} edited successfully!".format(category.name))
        return redirect(url_for('indexPage'))
    else:
        user = login_session['email']
        return render_template('edit_category.html',
                               category=category,
                               category_counts=category_counts, user=user)


@app.route('/categories/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    """ Delete an existing category """
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(id=category_id).one()
    category_counts = (
        session.query(Category.name, Category.id,
                      func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )

    if request.method == 'POST':
        session.delete(category)
        session.commit()
        flash("Category: {} deleted successfully!".format(category.name))
        return redirect(url_for('indexPage'))
    else:
        user = login_session['email']
        return render_template('delete_category.html',
                               category=category,
                               category_counts=category_counts, user=user)


# book view functions and corresponding JSON endpoint functions
@app.route('/categories/<int:category_id>/books-by-category')
def listBooksByCategory(category_id):
    """ Display books for a particular category """
    category = session.query(Category).filter_by(id=category_id).one()
    books = session.query(Book).filter_by(category_id=category_id)
    if 'username' not in login_session:
        return render_template('books_by_category_public.html',
                               books=books, category=category)
    else:
        user = login_session['email']
        return render_template('books_by_category.html', books=books,
                               category=category, user=user)


@app.route('/categories/<int:category_id>/books-by-category/JSON')
def listBooksByCategoryJSON(category_id):
    """ Display books for a particular category """
    category = session.query(Category).filter_by(id=category_id).one()
    books = session.query(Book).filter_by(category_id=category_id)
    # define empty list
    book_list = []
    for book in books:
        if book.category.id == category.id:
            # create a dictionary entry for each book that matches the category
            result = {
                    'Title': book.title,
                    'Author': book.author,
                    'Category': category.name,
                }
        book_list.append(result)
    # use jsonify the list and give it a key
    return jsonify(Books_by_Category=book_list)


@app.route('/books/<int:book_id>')
def singleBook(book_id):
    """ Display information about a particular book """
    book = session.query(Book).filter_by(id=book_id).one()
    categories = session.query(Category)
    titles = session.query(Book.id).order_by(Book.title).all()
    id_list = [x[0] for x in titles]

    if 'username' not in login_session:
        return render_template('single_book_public.html', book=book,
                               categories=categories, id_list=id_list)
    else:
        user = login_session['email']
        return render_template('single_book.html', book=book,
                               categories=categories,
                               id_list=id_list, user=user)


@app.route('/books/<int:book_id>/JSON')
def singleBookJSON(book_id):
    """ Display information about a particular book """
    book = session.query(Book).filter_by(id=book_id).one()
    categories = session.query(Category)
    # loop through the categories until it matches the queried book
    for category in categories:
        if category.id == book.category_id:
            # create a dictionary for the book info
            result = {
                            'Title': book.title,
                            'Author': book.author,
                            'Second Author': book.author2,
                            'Description': book.description,
                            'Category': category.name,
                        }
    # jsonify the dictionary for the endpoint display
    return jsonify(result)


# book create, update, delete functions
@app.route('/books/create', methods=['GET', 'POST'])
def createBook():
    """ Create a new book """
    if 'username' not in login_session:
        return redirect('/login')

    categories = session.query(Category).order_by(Category.name)
    titles = session.query(Book.id).order_by(Book.title).all()
    id_list = [x[0] for x in titles]

    if request.method == 'POST':
        new_book = Book(title=request.form['title'],
                        subtitle=request.form['subtitle'],
                        author=request.form['author'],
                        author2=request.form['author2'],
                        description=request.form['description'],
                        category_id=request.form['category_id']
                        )

        if not request.form['title'] or not request.form['author']:
            flash('Please fill out required form fields!')
            return redirect(url_for('createBook'))

        session.add(new_book)
        session.commit()
        flash("Book: {} created successfully!".format(new_book.title))
        return redirect(url_for('singleBook', book_id=new_book.id))
    else:
        user = login_session['email']
        return render_template('create_book.html',
                               categories=categories, user=user)


@app.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
def editBook(book_id):
    """ Edit an existing book """
    if 'username' not in login_session:
        return redirect('/login')

    book = session.query(Book).filter_by(id=book_id).one()
    categories = session.query(Category).order_by(Category.name)

    if request.method == 'POST':
        edit_book = ({'title': request.form['title'],
                      'subtitle': request.form['subtitle'],
                      'author': request.form['author'],
                      'author2': request.form['author2'],
                      'description': request.form['description'],
                      'category_id': request.form['category_id'],
                      })

        if not request.form['title'] or not request.form['author']:
            flash('Please fill out required form fields!')
            return redirect(url_for('editBook', book_id=book_id))

        session.query(Book).filter_by(id=book_id).update(edit_book)
        session.commit()
        flash("Book: {} edited successfully!".format(book.title))
        return redirect(url_for('singleBook', book_id=book_id))
    else:
        user = login_session['email']
        return render_template('edit_book.html', book=book,
                               categories=categories, user=user)


@app.route('/books/<int:book_id>/delete', methods=['GET', 'POST'])
def deleteBook(book_id):
    """ Delete a book and make it go bye bye """
    if 'username' not in login_session:
        return redirect('/login')

    book = session.query(Book).filter_by(id=book_id).one()
    books = session.query(Book).order_by(Book.title)
    category_counts = (
        session.query(Category.name, Category.id,
                      func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )

    if request.method == 'POST':
        session.delete(book)
        session.commit()
        flash("Book: {} deleted successfully!".format(book.title))
        return redirect(url_for('indexPage'))
    else:
        user = login_session['email']
        return render_template('delete_book.html',
                               book=book, books=books,
                               category_counts=category_counts, user=user)


# Oauth and login functions
@app.route('/login')
def showLogin():
    # create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current state is %s" % login_session['state']
    return render_template('login.html', STATE=state, CLIENT_ID=CLIENT_ID)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization data
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')

        # These values are pulled from environment variables
        oauth_flow.client_id = CLIENT_ID
        oauth_flow.client_secret = gclient_secret

        # statements for debugging - do we have the correct values?
        # print CLIENT_ID
        # print gclient_secret

        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

        # debug statement
        # print credentials.to_json()

    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401
            )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check and see is access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify the access token is for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps
                                 ("Token doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's"
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    # debug statement
    # print data

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if local user exists, if it doesn't make a new one

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # debug statements
    # print "The user id is:"
    # print user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += (''' " style = "width: 300px; height: 300px;
               border-radius: 150px; -webkit-border-radius:
               150px;-moz-border-radius: 150px;"> '''
               )
    flash("you are now logged in as %s" % login_session['email'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')

    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-type'] = 'application/json'
        # return response
        flash("Current user is not logged in")
        return redirect(url_for('indexPage'))

    # statements for debugging
    # print 'In gdisconnect access token is:'
    # print access_token
    # print
    # print 'User name is: '
    # print login_session['username']
    # print
    # print 'full login_session info:'
    # print login_session

    url = ("https://accounts.google.com/o/oauth2/revoke?token=%s"
           % login_session['access_token'])

    # statements for debugging
    # print
    # print 'url is:'
    # print url

    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # Yet more debugging with print
    # print
    # print 'result of GET request to url is: '
    # print result

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        # return response
        # instead of returning response, we'll flash and redirect to index
        flash("You have successfully logged out")
        return redirect(url_for('indexPage'))

    else:
        # we are only getting this condition after 1 hour token expiry
        # so we're going to change this to just log the user out anyway

        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        # return response
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        # response.headers['Content-Type'] = 'application/json'
        flash(""" You have successfully logged out, although your token was unable.
              to be revoked, probably because it expired after one hour. Nothing to
              worry about really, just thought I'd share.""")
        print "token expired"
        return redirect(url_for('indexPage'))


# Local user helper functions
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
