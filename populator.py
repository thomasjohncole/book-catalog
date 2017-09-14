from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Category, Book
#from flask.ext.sqlalchemy import SQLAlchemy

engine = create_engine('sqlite:///books.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#Add categories
category1 = Category(name = "SciFi")
session.add(category1)

category2 = Category(name = "Technology")
session.add(category2)

category3 = Category(name = "Self Help")
session.add(category3)

category4 = Category(name = "General Non-Fiction")
session.add(category4)

category5 = Category(name = "Fiction")
session.add(category5)

category6 = Category(name = "Psychology")
session.add(category6)

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

book4 = Book(title = "In Search of Certainty",
             subtitle = "The Science of Our Information Infrastructure",
             author = "Mark Burgess",
             description = "Ex-Pysicist's philosphical treatise on configuration management.",
             category_id = "2")
session.add(book4)

book5 = Book(title = "Deep Work",
             subtitle = "Rules for Focused Success in a Distracted World",
             author = "Cal Newport",
             description = "Learning how to focus on cognitively demanding tasks will pay dividends.",
             category_id = "3")
session.add(book5)

book6 = Book(title = "To Kill a Mockingbird",
             author = "Harper Lee",
             description = "A child's view of life in the post-depression deep south.",
             category_id = "5")
session.add(book6)



session.commit()
