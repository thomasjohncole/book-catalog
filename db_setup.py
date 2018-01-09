import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
# creates three tables with the specified columns #

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """ returns serialized object data """
        return {
            'name' : self.name,
            'id' : self.id,
            'many2many' : self.serialize_many2many,
        }

    @property
    def serialize_many2many(self):
       """
       Return object's relations in easily serializeable format.
       NB! Calls many2many's serialize property.
       """
       return [ item.serialize for item in self.many2many]

class Book(Base):
    __tablename__ = 'book'

    title = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    subtitle = Column(String(250))
    author = Column(String(250), nullable = False)
    author2 = Column(String(250))
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """ returns serialized object data """
        return {
            'title' : self.title,
            'subtitle' : self.subtitle,
            'id' : self.id,
            'author' : self.author,
            'author2' : self.author2,
            'description' : self.description,
            'category_id' : self.category_id,
        }



# creates the database #
engine = create_engine( 'sqlite:///books.db')

Base.metadata.create_all(engine)
