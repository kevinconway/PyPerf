import falcon

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyperf.models import Base
from pyperf.wsgi.entries import EntryCollection
from pyperf.wsgi.entries import EntryInstance


def make_app(db_engine=None):

    Session = sessionmaker()
    engine = db_engine or create_engine('sqlite://')
    Session.configure(bind=engine)

    Base.metadata.create_all(engine)

    app = falcon.API()

    app.add_route('/entries', EntryCollection(Session))
    app.add_route('/entries/{entry_slug}', EntryInstance(Session))

    return app
