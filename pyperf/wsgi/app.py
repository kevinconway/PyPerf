import falcon

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..models import Base
from .resources.entries import EntryCollection
from .resources.entries import EntryInstance


def make_app(db_engine=None, transport=None):

    if transport is None:

        raise ValueError('The transport cannot be None.')

    Session = sessionmaker()
    engine = db_engine or create_engine('sqlite://')
    Session.configure(bind=engine)

    Base.metadata.create_all(engine)

    app = falcon.API()

    app.add_route('/entries', EntryCollection(Session, transport))
    app.add_route('/entries/{entry_slug}', EntryInstance(Session, transport))

    return app
