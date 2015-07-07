"""Transport implementation using amqp."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json

import amqp

from ..interfaces import transport
from .. import messages


class AmqpTransport(transport.Transport):

    """Transport interface implementation using amqp."""

    def __init__(self, host, username, password, queue):
        """Initialize the transport with connection data."""
        self._connection = amqp.Connection(
            host,
            userid=username,
            password=password,
        )
        self._channel = self._connection.channel()
        self._queue = queue
        self._channel.queue_declare(self._queue)
        self._message_map = {}

    def send(self, message):
        """Send a single message over the transport."""
        msg = amqp.Message(
            json.dumps(message.json),
            content_type='application/json',
        )
        self._channel.basic_publish(msg, routing_key=self._queue)

    def fetch(self):
        """Fetch a single message from the transport."""
        payload = self._channel.basic_get(self._queue)
        if payload is None:
            return None
        message = messages.from_json(json.loads(payload.body))
        self._message_map[message] = payload
        return message

    def complete(self, message):
        """Mark a message as complete on the transport."""
        payload = self._message_map.pop(message)
        self._channel.basic_ack(payload.delivery_tag)

    def close(self):
        """Close the AMQP connection."""
        self._connection.close()
