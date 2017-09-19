import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
# creates two tables with the specified columns #
class Category(Base):
    __tablename__ = 'category'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

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
        }



# creates the database #
engine = create_engine( 'sqlite:///books.db')

Base.metadata.create_all(engine)
