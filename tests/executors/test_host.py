from collections import deque
import unittest
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyperf.executor.host import HostExecutor
from pyperf.models import Base
from pyperf.models import Entry
from pyperf.models import Snippet
from pyperf.models import Result
from pyperf.profile.interfaces import ProfileResults
from pyperf.transport.interfaces import Transport
from pyperf.transport.messages import ProfileRequest


class FakeTransport(Transport):

    def __init__(self):

        self._q = deque()
        self._complete = []

    def send(self, message):

        self._q.append(message.json())

    def fetch(self):

        return self._q.popleft()

    def complete(self, message):

        self._complete.append(message)

    def close(self):

        pass


class TestHostExecutor(unittest.TestCase):

    def setUp(self):

        self._Session = sessionmaker()
        engine = create_engine('sqlite://')
        self._Session.configure(bind=engine)
        Base.metadata.create_all(engine)

        self._transport = FakeTransport()

        self._entry = Entry(
            identity=str(uuid.uuid4()),
            setup='pass',
            name='test',
        )
        session = self._Session()
        session.add(self._entry)
        session.commit()

    def _make_executor(self):

        random = str(uuid.uuid4())
        return HostExecutor(
            '/tmp/' + random,
            transport=self._transport,
            samples=1,
            Session=self._Session,
        )

    def _make_snippet(self):

        session = self._Session()
        snippet = Snippet(
            entry_identity=self._entry.identity,
            code='for x in range(100000): pass',
        )
        session.add(snippet)
        session.commit()
        return snippet

    def test_profiles_request(self):

        snippet = self._make_snippet()

        request = ProfileRequest(
            identity=snippet.identity,
            setup=self._entry.setup,
            code=snippet.code,
        )
        e = self._make_executor()

        results = e.handle_profile_request(request)

        self.assertTrue(isinstance(results, ProfileResults))
        self.assertTrue(results.runtime > 0)
        self.assertTrue(results.memory.max > 0)

    def test_pulls_from_transport(self):

        self._transport.send(ProfileRequest(0, 'test', 'test'))
        e = self._make_executor()

        message = e.get_message()

        self.assertTrue(message.identity == 0)
        self.assertTrue(message.setup == 'test' and message.code == 'test')

    def test_updates_results_record(self):

        snippet = self._make_snippet()

        request = ProfileRequest(
            identity=snippet.identity,
            setup=self._entry.setup,
            code=snippet.code,
        )
        e = self._make_executor()

        results = e.handle_profile_request(request)

        e.update_results(message=request, results=results)

        session = self._Session()
        record = session.query(Result).filter(
            Result.snippet_identity == snippet.identity
        ).first()

        self.assertTrue(record is not None)
        self.assertTrue(record.runtime == results.runtime)
        self.assertTrue(record.max_memory == results.memory.max)
