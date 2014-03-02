from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Unicode
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship


Base = declarative_base()


class Result(Base):

    __tablename__ = 'results'

    snippet_identity = Column(
        Integer,
        ForeignKey('snippets.identity'),
        primary_key=True,
    )
    runtime = Column(Float)
    max_memory = Column(Float)
    avg_memory = Column(Float)
    min_memory = Column(Float)


class Snippet(Base):

    __tablename__ = 'snippets'

    entry_identity = Column(Unicode(64), ForeignKey('entries.identity'))
    identity = Column(Integer, primary_key=True)
    code = Column(Text)

    result = relationship("Result", uselist=False, backref="snippet")


class Entry(Base):

    __tablename__ = 'entries'

    # identity is also a slug useful for URLs.
    identity = Column(Unicode(64), primary_key=True)
    name = Column(Unicode(64))
    setup = Column(Text)
    snippets = relationship("Snippet", backref='entry')
