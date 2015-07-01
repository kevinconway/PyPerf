"""Standard interface for message transports."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class Transport(object):

    """Standard interface for message transports."""

    def send(self, message):
        """Send a single message on the transport.

        Args:
            message (Message): Some implementation of the message interface.
        """
        raise NotImplementedError()

    def fetch(self):
        """Fetch a single message from the transport.

        Returns:
            Message: Some implementation of the message interface.
        """
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
        raise NotImplementedError()
