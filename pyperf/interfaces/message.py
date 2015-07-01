"""Message interfaces."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class Message(object):

    """Standard interface for messages."""

    message_type = None

    @property
    def identifier(self):
        """Get the unique message identifier."""
        raise NotImplementedError()

    @property
    def json(self):
        """Fetch a JSON serializable of the message."""
        raise NotImplementedError()

    @classmethod
    def from_json(cls, json):
        """Create a new message from the JSON payload."""
        raise NotImplementedError()
