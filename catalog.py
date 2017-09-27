from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
Bootstrap(app)

from sqlalchemy import create_engine, func, update
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, Book

engine = create_engine('sqlite:///books.db')
Base.metadata.bind = engine
# binds the engine to the Base class
# makes the connections between class definitions & corresponding tables in db
DBSession = sessionmaker(bind = engine)
# creates sessionmaker object, which establishes link of
# communication between our code executions and the engine we created
session = DBSession()
# create an instance of the DBSession  object - to make a changes
# to the database, we can call a method within the session

@app.route('/')
def indexPage():
    """ Shows a list of categories and a list of books """
    books = session.query(Book).order_by(Book.title)
    category_counts = (
        session.query(Category.name, Category.id, func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )
    return render_template('index.html',books = books, category_counts = category_counts)

# category stuff

@app.route('/categories/create', methods=['GET','POST'])
def createCategory():
    """ Create a new category """
    category_counts = (
        session.query(Category.name, Category.id, func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )

    if request.method == 'POST':
        new_category = Category(name = request.form['category_name'])
        session.add(new_category)
        session.commit()
        return redirect(url_for('indexPage'))
    else:
        return render_template('create_category.html', category_counts = category_counts)


@app.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    """ Edit the name of an existing category """
    category = session.query(Category).filter_by(id = category_id).one()
    category_counts = (
        session.query(Category.name, Category.id, func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )

    if request.method == 'POST':
        data = ({"name": request.form['category_name']})
        session.query(Category).filter_by(id = category_id).update(data)
        session.commit()
        return redirect(url_for('indexPage'))
    else:
        return render_template('edit_category.html',
            category = category, category_counts = category_counts)


@app.route('/categories/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    """ Delete an existing category """
    category = session.query(Category).filter_by(id = category_id).one()
    category_counts = (
        session.query(Category.name, Category.id, func.count(Book.title).label("count"))
        .outerjoin(Book, Category.id == Book.category_id)
        .group_by(Category.id)
        .order_by(Category.name)
        )

    if request.method == 'POST':
        session.delete(category)
        session.commit()
        return redirect(url_for('indexPage'))
    else:
        return render_template('delete_category.html',
            category = category, category_counts = category_counts)


# book stuff

@app.route('/categories/<int:category_id>/books')
def listBooks(category_id):
    """ List books for a particular category """
    category = session.query(Category).filter_by(id = category_id).one()
    books = session.query(Book).filter_by(category_id = category_id)
    return render_template('books_by_category.html', books = books, category = category)

@app.route('/books/<int:book_id>')
def singleBook(book_id):
    book = session.query(Book).filter_by(id = book_id).one()
    categories = session.query(Category)
    titles = session.query(Book.id).order_by(Book.title).all()
    id_list = [x[0] for x in titles]

    return render_template('single_book.html',
                            book = book,
                            categories = categories,
                            id_list = id_list)


@app.route('/books/create', methods=['GET', 'POST'])
def createBook():
    """ Create a new book """
    categories = session.query(Category)

    if request.method == 'POST':
        new_book = Book(title = request.form['title'],
                        subtitle = request.form['subtitle'],
                        author = request.form['author'],
                        author2 = request.form['author2'],
                        description = request.form['description'],
                        category_id = request.form['category_id']
                           )
        session.add(new_book)
        session.commit()
        return redirect(url_for('indexPage'))
    else:
        return render_template('create_book.html', categories = categories)


@app.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
def editBook(book_id):
    """ Edit an existing book """
    book = session.query(Book).filter_by(id = book_id).one()
    categories = session.query(Category)

    if request.method == 'POST':
        edit_book = ({'title': request.form['title'],
                      'subtitle': request.form['subtitle'],
                      'author':request.form['author'],
                      'author2': request.form['author2'],
                      'description': request.form['description'],
                      'category_id': request.form['category_id']}
                           )
        session.query(Book).filter_by(id = book_id).update(edit_book)
        session.commit()
        return redirect(url_for('singleBook', book_id = book_id))
    else:
        return render_template('edit_book.html', book = book, categories = categories)

@app.route('/books/<int:book_id>/delete', methods=['GET', 'POST'])
def deleteBook(book_id):
    """ Delete a book and make it go bye bye """
    book = session.query(Book).filter_by(id = book_id).one()

    if request.method == 'POST':
        session.delete(book)
        session.commit()
        return redirect(url_for('indexPage'))
    else:
        return render_template('delete_book.html', book = book)


# Oauth stuff

@app.route('/login')
def gconnect():
    return "This is the URL for authentication via Google+ OAuth 2"

@app.route('/disconnect')
def gdisconnect():
    return "This is the URL for disconnecting from Google OAuth 2"

# JSON stuff

@app.route('/json')
def indexPageJSON():
    return "This is the JSON data for the index page!"

@app.route('/categories/books/JSON')
def listBooksJSON():
    return "This is the JSON data for the books list page for a particular category!"


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)




