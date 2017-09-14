from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from book_db_setup import Base, Category, Book
#from flask.ext.sqlalchemy import SQLAlchemy

engine = create_engine('sqlite:///books.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#Add categories
category1 = Category(name = "SciFi")
session.add(category1)

#Add books
book1 = Book(title = "Excession",
             author = "Ian Banks",
             description = "An object appears which threatens the stability of the universe.",
             category_id = "1")
session.add(book1)

book2 = Book(title = "The Dosadai Experiment",
             author = "Frank Herbert",
             description = "A secret experiment on a secret planet gets way out of hand.",
             category_id = "1")
session.add(book2)

book3 = Book(title = "Starfish",
             author = "Peter Watts",
             description = "Modified humans living in the deep sea experience ganzfeld effects.",
             category_id = "1")
session.add(book3)



session.commit()
