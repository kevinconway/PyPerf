import json

from .messages import ProfileRequest


class Transport(object):

    def send(self, message):
        """Send a single message on the transport."""

        raise NotImplementedError()

    def fetch(self):
        """Fetch a single message from the transport."""

        raise NotImplementedError()

    def complete(self, message):
        """Finalize a message from a transport.

        This method may not do anything depending on the transport being
        implemented. The motivation behind this method is to allow transports
        with transactional messaging to finalize transactions if needed.

        Example: AMQP ack.

        """

        raise NotImplementedError()

    def close(self):
        """Terminate connection to transport if applicable."""

    def message_from_payload(self, payload):

        payload = json.loads(payload)
        message_type = payload.get('type')

        if message_type == 'profile_request':

            return ProfileRequest(
                identity=payload['identity'],
                setup=payload['setup'],
                code=payload['code'],
            )

        raise ValueError(
            'Message type ({0}) not recognized.'.format(message_type)
        )
