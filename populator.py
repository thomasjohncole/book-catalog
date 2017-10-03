from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Category, Book
#from flask.ext.sqlalchemy import SQLAlchemy

engine = create_engine('sqlite:///books.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#Add categories
category1 = Category(name = "Science Fiction")
session.add(category1)

category2 = Category(name = "Technology")
session.add(category2)

category3 = Category(name = "Psych/Self Help")
session.add(category3)

category4 = Category(name = "Non Fiction")
session.add(category4)

category5 = Category(name = "Fiction")
session.add(category5)


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

book4 = Book(title = "Machine, Platform, Crowd",
             subtitle = "Harnessing Our Digital Future",
             author = "Andrew McAfee",
             author2 = "Erik Brynjolfsson",
             description = "A survey of technological trends influencing the modern global economy.",
             category_id = "2")
session.add(book4)

book5 = Book(title = "Race Against the Machine",
             subtitle = "How the Digital Revolution Is Accelerating Innovation, Driving Productivity, and Irreversibly Transforming Employment and the Economy.",
             author = "Erik Brynjolfsson",
             author2 = "Andrew McAfee ",
             description = "Some good insights on how not to lose your job to a machine.",
             category_id = "2")
session.add(book5)

book6 = Book(title = "In Search of Certainty",
             subtitle = "The Science of Our Information Infrastructure",
             author = "Mark Burgess",
             description = "Ex-Pysicist's philosphical treatise on configuration management.",
             category_id = "2")
session.add(book6)

book7 = Book(title = "Deep Work",
             subtitle = "Rules for Focused Success in a Distracted World",
             author = "Cal Newport",
             description = "Learning how to focus on cognitively demanding tasks will pay dividends.",
             category_id = "3")
session.add(book7)

book8 = Book(title = "Grit",
             subtitle = "The Power of Passion and Perseverance",
             author = "Angela Duckworth",
             description = "Hard work and persistence matter more than IQ when accomplishing goals.",
             category_id = "3")
session.add(book8)

book9 = Book(title = "So Good They Can't Ignore You",
             subtitle = "Why Skills Trump Passion in the Quest for Work You Love",
             author = "Cal Newport",
             description = "Get skillz, build career capital, then you are in a better position to pursue rewarding vocational engagement.",
             category_id = "3")
session.add(book9)

book10 = Book(title = "Thinking, Fast and Slow",
             author = "Daniel Kahneman",
             description = "We have two systems of thinking, which often contradict each other.",
             category_id = "4")
session.add(book10)

book11 = Book(title = "Molecules of Emotion",
             subtitle = "The Science Behind Mind-Body Medicine",
             author = "Candace Pert",
             description = "An autobiographical account of the world of biological research.",
             category_id = "4")
session.add(book11)

book12 = Book(title = "Plotinus",
             author = "AH Armstrong",
             description = "A brief analysis of the works of one of the best known Neo-Platonist philosophers.",
             category_id = "4")
session.add(book12)

book13 = Book(title = "The Unbearable Lightness of Being",
             author = "Milan Kundera",
             description = "Life, love, and loss during the time of the Prague Spring.",
             category_id = "5")
session.add(book13)

book14 = Book(title = "Animal Farm",
             author = "George Orwell",
             description = "A metaphorical fiction describing the dark side of utopian idealism.",
             category_id = "5")
session.add(book14)

book15 = Book(title = "To Kill a Mockingbird",
             author = "Harper Lee",
             description = "A child's view of life in the post-depression deep south.",
             category_id = "5")
session.add(book15)

session.commit()
