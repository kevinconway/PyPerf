"""Transport implementation using amqp."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json

import amqp
import confpy.api

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
            message.json,
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
        del self._message_map[message]

    def close(self):
        """Close the AMQP connection."""
        self._connection.close()


confpy.api.Configuration(
    amqp=confpy.api.Namespace(
        description="AMQP transport configuration options.",
        host=confpy.api.StringOption(
            description="The hostname of the AMQP endpoint.",
        ),
        username=confpy.api.StringOption(
            description="The username to use when authenticating.",
        ),
        password=confpy.api.StringOption(
            description="The password to use when authenticating.",
        ),
        queue=confpy.api.StringOption(
            description="The queue to send/read from.",
        ),
    ),
)


def amqp_driver(config):
    """Driver interface for the AmqpTransport."""
    return AmqpTransport(
        host=config.amqp.host,
        username=config.amqp.username,
        password=config.amqp.password,
        queue=config.amqp.queue,
    )
