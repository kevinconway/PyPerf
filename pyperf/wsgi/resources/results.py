import json

import falcon

from ...models import Entry

from .base import BaseResource


class ResultCollection(BaseResource):

    def on_get(self, req, resp, entry_slug):
        """List all results for the entry."""

        session = self.Session()
        query = session.query(Entry).filter(Entry.identity == entry_slug)
        entry = query.first()

        if entry is None:

            resp.status = falcon.HTTP_404
            resp.body = "Entry not found."

            return

        resp.body = json.dumps(
            {
                "id": entry.identity,
                "name": entry.name,
                "setup": entry.setup,
                "snippets": tuple(
                    {
                        "code": s.code,
                        "runtime": s.result.runtime,
                        "memory": {
                            "avg": s.result.avg_memory,
                            "max": s.result.max_memory,
                            "min": s.result.min_memory,
                        },
                    } if s.result is not None else {
                        "code": s.code,
                        "runtime": None,
                        "memory": {
                            "avg": None,
                            "max": None,
                            "min": None,
                        },
                    } for s in entry.snippets
                ),
            }
        )
