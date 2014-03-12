import json
import unittest

from falcon.testing.helpers import create_environ
from falcon.testing.srmock import StartResponseMock

from pyperf.wsgi.app import make_app


class FakeTransport(object):

    def send(self, message):

        pass

    def fetch(self):

        pass

    def complete(self, message):

        pass

    def close(self):

        pass


class TestBasicProfile(unittest.TestCase):

    def setUp(self):

        self.app = make_app(transport=FakeTransport())

    def test_can_list_all_entries(self):

        results = self.app(
            create_environ(
                path='/entries',
            ),
            StartResponseMock(),
        )[0].decode()

        results = json.loads(results)

        try:

            for r in results:

                pass

        except TypeError:

            raise AssertionError('API results are not iterable.')

    def test_create_errors_when_json_invalid(self):

        start_response = StartResponseMock()

        self.app(
            create_environ(
                path='/entries',
                method='POST',
                body='{{[[[}}]',
            ),
            start_response,
        )[0].decode()

        self.assertTrue(start_response.status == '400 Bad Request')

    def test_create_errors_when_payload_invalid(self):

        start_response = StartResponseMock()

        self.app(
            create_environ(
                path='/entries',
                method='POST',
                body='{"name": "test"}',  # Missing values
            ),
            start_response,
        )[0].decode()

        self.assertTrue(start_response.status == '400 Bad Request')

    def test_create_succeeds_when_payload_correct(self):

        start_response = StartResponseMock()

        result = self.app(
            create_environ(
                path='/entries',
                method='POST',
                body=json.dumps(
                    {
                        "name": "test correct payload",
                        "setup": "pass",
                        "snippets": ("pass", "pass")
                    }
                ),
            ),
            start_response,
        )[0].decode()
        result = json.loads(result)

        self.assertTrue(start_response.status == '201 Created')
        self.assertTrue(result['id'] == 'test_correct_payload')

    def test_create_can_be_retrieved_later(self):

        payload = {
            "name": "test can be retrieved",
            "setup": "pass",
            "snippets": ("pass", "pass")
        }

        start_response = StartResponseMock()
        result = self.app(
            create_environ(
                path='/entries',
                method='POST',
                body=json.dumps(payload),
            ),
            start_response,
        )[0].decode()
        result = json.loads(result)

        start_response2 = StartResponseMock()
        result2 = self.app(
            create_environ(
                path='/entries/{0}'.format(result['id']),
            ),
            start_response2,
        )[0].decode()
        result2 = json.loads(result2)

        self.assertTrue(start_response2.status != '404 Not Found')
        self.assertTrue(result2['id'] == result['id'])
        self.assertTrue(result2['name'] == payload['name'])
        self.assertTrue(result2['setup'] == payload['setup'])

        for snip1, snip2 in zip(payload['snippets'], result2['snippets']):
            self.assertTrue(snip1 == snip2)
