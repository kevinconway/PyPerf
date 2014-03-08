import amqp

from .interfaces import Transport


class AmqpTransport(Transport):

    def __init__(self, host, username, password, queue):

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

        msg = amqp.Message(
            message.json(),
            content_type='application/json',
        )

        self._channel.basic_publish(msg, routing_key=self._queue)

    def fetch(self):

        payload = self._channel.basic_get(self._queue)
        if payload is None:
            return None
        message = self.message_from_payload(payload.body)
        self._message_map[message] = payload
        return message

    def complete(self, message):

        payload = self._message_map[message]
        self._channel.basic_ack(payload.delivery_tag)
        del self._message_map[message]

    def close(self):

        self._connection.close()
