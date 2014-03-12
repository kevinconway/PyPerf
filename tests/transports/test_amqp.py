import unittest
import uuid

import amqp

from pyperf.transport.amq import AmqpTransport
from pyperf.transport.messages import ProfileRequest


class TestAmqpTransport(unittest.TestCase):

    def setUp(self):

        # Roll a UUID to keep this test suite seperate from reapeat runs.
        self._test_id = str(uuid.uuid4())

        # Create a raw amqp connection to use in tests.
        connection = amqp.Connection(
            'localhost',
            userid='guest',
            password='guest',
        )
        self._channel = connection.channel()
        self._channel.queue_declare(self._test_id)

    def test_can_place_message_on_queue(self):

        # Roll a UUID to make sure we're getting the right message.
        secret = str(uuid.uuid4())

        # Generate a transport and place a message on the queue.
        trans = AmqpTransport(
            host='localhost',
            username='guest',
            password='guest',
            queue=self._test_id,
        )

        message = ProfileRequest(0, secret, secret)
        trans.send(message)

        # Use the raw client to fetch to message.
        # Placed in a while loop to prevent false test failures due to
        # occasional race conditions.
        raw_message = None
        while raw_message is None:
            raw_message = self._channel.basic_get(self._test_id)
        # Find the secret.
        self.assertTrue(secret in raw_message.body)
        # ACK the message to avoid breaking other tests.
        self._channel.basic_ack(raw_message.delivery_tag)

    def test_can_fetch_message_from_queue(self):

        secret = str(uuid.uuid4())

        raw_message = amqp.Message(
            ProfileRequest(0, secret, secret).json(),
            content_type='application/json',
        )
        self._channel.basic_publish(raw_message, routing_key=self._test_id)

        trans = AmqpTransport(
            host='localhost',
            username='guest',
            password='guest',
            queue=self._test_id,
        )

        message = trans.fetch()
        self.assertTrue(message.code == secret)
        self._channel.basic_ack(trans._message_map[message].delivery_tag)

    def test_raises_value_error_on_unknown_message(self):

        raw_message = amqp.Message(
            '{"fake": true}',
            content_type='application/json',
        )
        self._channel.basic_publish(raw_message, routing_key=self._test_id)

        trans = AmqpTransport(
            host='localhost',
            username='guest',
            password='guest',
            queue=self._test_id,
        )

        with self.assertRaises(ValueError):

            trans.fetch()

        # Close the connection and force requeue of the message.
        trans.close()

        raw_message = self._channel.basic_get(self._test_id)
        self._channel.basic_ack(raw_message.delivery_tag)

    def test_can_ack_messages(self):

        raw_message = amqp.Message(
            ProfileRequest(0, '', '').json(),
            content_type='application/json',
        )
        self._channel.basic_publish(raw_message, routing_key=self._test_id)

        trans = AmqpTransport(
            host='localhost',
            username='guest',
            password='guest',
            queue=self._test_id,
        )

        message = trans.fetch()
        trans.complete(message)

        self.assertTrue(trans.fetch() is None)
