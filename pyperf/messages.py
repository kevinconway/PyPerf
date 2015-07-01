"""Message implementations."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import stevedore.extension

from .interfaces import message


class ProfileRequest(message.Message):

    """Message implementation that contains a request for code profiling."""

    message_type = "profile_request"

    def __init__(self, identifier, setup, code):
        """Initialize the ProfileRequest with relevant data.

        Args:
            identifier (str): Some unique identifier for the message.
            setup (str): The setup code for the profile.
            code (str): The target code for the profile.
        """
        self._identifier = identifier
        self._setup = setup
        self._code = code

    @property
    def identifier(self):
        """Get the unique message identifier."""
        return self._identifier

    @property
    def setup(self):
        """Get the setup code for the profile."""
        return self._setup

    @property
    def code(self):
        """Get the target code for the profile."""
        return self._code

    @property
    def json(self):
        """Get a JSON serializable form of the message."""
        return {
            "identifier": self.identifier,
            "setup": self.setup,
            "code": self.code,
            "message_type": self.__class__.message_type,
        }

    @classmethod
    def from_json(cls, payload):
        """Generate a message from a deserialized JSON payload."""
        return cls(
            identifier=payload['identifier'],
            setup=payload['setup'],
            code=payload['code'],
        )


class ProfileResult(ProfileRequest):

    """Message implementation that contains the results of a profile."""

    message_type = 'profile_result'

    def __init__(self, identifier, setup, code, value, unit):
        """Initialize the message with relevant data.

        Args:
            identifier (str): Some unique identifier for the message.
            setup (str): The setup code for the profile.
            code (str): The target code for the profile.
            value (number): The measured value of the profile.
            unit (str): The unit of measurement used in the profile.
        """
        super(ProfileResult, self).__init__(identifier, setup, code)
        self._value = value
        self._unit = unit

    @property
    def value(self):
        """Get the measured value of the profile."""
        return self._value

    @property
    def unit(self):
        """Get the unit of measurement used in the profile."""
        return self._unit

    @property
    def json(self):
        """Get a JSON serializable form of the message."""
        return {
            "identifier": self.identifier,
            "setup": self.setup,
            "code": self.code,
            "value": self.value,
            "unit": self.unit,
            "message_type": self.__class__.message_type,
        }

    @classmethod
    def from_json(cls, payload):
        """Generate a message from a deserialized JSON payload."""
        return cls(
            identifier=payload['identifier'],
            setup=payload['setup'],
            code=payload['code'],
            value=payload['value'],
            unit=payload['unit'],
        )


class ProfileFailure(ProfileRequest):

    """Message implementation that contains a failure report."""

    message_type = 'profile_failure'

    def __init__(self, identifier, setup, code, message):
        """Initialize the message with relevant data.

        Args:
            identifier (str): Some unique identifier for the message.
            setup (str): The setup code for the profile.
            code (str): The target code for the profile.
            message (str): The failure message.
        """
        super(ProfileFailure, self).__init__(identifier, setup, code)
        self._message = message

    @property
    def message(self):
        """Get the failure message."""
        return self._message

    @property
    def json(self):
        """Get a JSON serializable form of the message."""
        return {
            "identifier": self.identifier,
            "setup": self.setup,
            "code": self.code,
            "message": self.message,
            "message_type": self.__class__.message_type,
        }

    @classmethod
    def from_json(cls, payload):
        """Generate a message from a deserialized JSON payload."""
        return cls(
            identifier=payload['identifier'],
            setup=payload['setup'],
            code=payload['code'],
            message=payload['message'],
        )


def from_json(payload):
    """Convert a serialized JSON payload into a message object.

    This method leverages setuptools entry_points to load all available
    message types bound to the entry_point "pyperf_messages". Once a message
    with the appropriate type is found it is used to construct the message.

    Args:
        payload (dict): A serialized JSON payload of a message.

    Returns:
        Message: An implementation of the Message interface.

    Raises:
        ValueError: If the message type is missing from the payload
        TypeError: If the message type is not found in the entry_point.
    """
    if 'message_type' not in payload:

        raise ValueError('Missing message_type value in the payload.')

    target_type = payload['message_type']
    message_implementations = stevedore.extension.ExtensionManager(
        namespace='pyperf_messages',
        invoke_on_load=False,
    )

    for implementation in message_implementations:

        if implementation.plugin.message_type == target_type:

            return implementation.plugin.from_json(payload)

    raise TypeError("Message of type {0} not found.".format(target_type))
