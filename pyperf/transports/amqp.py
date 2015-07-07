"""Transport implementation using amqp."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import functools
import json
import socket

import amqp

from ..interfaces import transport
from .. import messages


def _retry_if_socket_failure(transport_func):
    """Regenerate the connection information and retry during a sock error."""
    @functools.wraps(transport_func)
    def _regen_and_retry(self, *args, **kwargs):
        """Generate new connection info and retry."""
        while True:

            try:

                return transport_func(self, *args, **kwargs)

            except socket.error:

                self._connect()
                continue

    return _regen_and_retry


class AmqpTransport(transport.Transport):

    """Transport interface implementation using amqp."""

    def __init__(self, host, username, password, queue):
        """Initialize the transport with connection data."""
        self._host = host
        self._username = username
        self._password = password
        self._queue = queue
        self._connect()
        self._message_map = {}

    def _connect(self):
        """Generate connection information."""
        self._connection = amqp.Connection(
            self._host,
            userid=self._username,
            passowrd=self._password,
        )
        self._channel = self._connection.channel()
        self._channel.queue_declare(self._queue)

    @_retry_if_socket_failure
    def send(self, message):
        """Send a single message over the transport."""
        msg = amqp.Message(
            json.dumps(message.json),
            content_type='application/json',
        )
        self._channel.basic_publish(msg, routing_key=self._queue)

    @_retry_if_socket_failure
    def fetch(self):
        """Fetch a single message from the transport."""
        payload = self._channel.basic_get(self._queue, no_ack=True)
        if payload is None:
            return None
        message = messages.from_json(json.loads(payload.body))
        # self._message_map[message.identifier] = payload
        return message

    @_retry_if_socket_failure
    def complete(self, message):
        """Mark a message as complete on the transport."""
        return None
        # payload = self._message_map.get(message.identifier)
        # self._channel.basic_ack(payload.delivery_tag)
        # self._message_map.pop(message.identifier)

    def close(self):
        """Close the AMQP connection."""
        self._connection.close()
