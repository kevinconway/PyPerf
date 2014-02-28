"""Silly flatfile store until db is ready."""

import json
import os


class Store(object):

    def __init__(self, path='/tmp/sample_store.json'):

        if not os.path.exists(path):

            self._store = open(path, 'w+')

        else:

            self._store = open(path, 'r+')

        if not len(self._store.read()):

            self._store.write('[]')

        self._store.seek(0)

    def get_all(self):

        self._store.seek(0)
        return json.loads(self._store.read())

    def get(self, sample_id):

        self._store.seek(0)
        try:

            return tuple(
                s for s in json.loads(self._store.read())
                if s['id'] == sample_id
            )[0]

        except IndexError:

            return None

    def add(self, sample):

        self._store.seek(0)
        values = json.loads(self._store.read())
        values.append(sample)

        self._store.seek(0)
        self._store.write(json.dumps(values))
