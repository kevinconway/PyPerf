import json

import falcon

from ..models import Entry
from ..models import Snippet

from .base import DbResource


class EntryCollection(DbResource):

    def on_get(self, req, resp):
        """List all current entry identities."""

        session = self.Session()
        query = session.query(Entry.identity, Entry.name)
        resp.body = json.dumps(
            tuple(
                {"id": r.identity, "name": r.name}
                for r in query
            )
        )

    def on_post(self, req, resp):
        """Create a new entry."""

        try:

            body = req.stream.read().decode()
            new_entry = json.loads(body)

        except ValueError:

            raise falcon.HTTPError(
                falcon.HTTP_400,
                'Malformed JSON.',
            )

        try:

            entry = Entry(
                name=new_entry['name'],
                setup=new_entry['setup'],
                identity=''.join(
                    c if c.isalnum() else '_'
                    for c in new_entry['name']
                ),
            )
            entry.snippets = [
                Snippet(code=c)
                for c in new_entry['snippets']
            ]

        except:

            raise falcon.HTTPError(
                falcon.HTTP_400,
                'Invalid input.',
            )

        session = self.Session()
        session.add(entry)
        session.commit()

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({"id": entry.identity})


class EntryInstance(DbResource):

    def on_get(self, req, resp, entry_slug):
        """Get details of an entry."""

        session = self.Session()
        query = session.query(Entry)
        query = query.filter(Entry.identity == entry_slug)
        result = query.first()

        if result is None:

            resp.status = falcon.HTTP_404
            resp.body = "Entry not found."

        resp.body = json.dumps(
            {
                "id": result.identity,
                "name": result.name,
                "setup": result.setup,
                "snippets": [
                    s.code for s in result.snippets
                ]
            }
        )
