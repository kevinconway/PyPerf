"""Daemons that leverage the profiler interface."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from .. import messages
from . import base


class ProfilerDaemon(base.BaseDaemon):

    """Daemon that profiles code."""

    def __init__(self, *args, **kwargs):
        """Initialize the daemon with a profiler."""
        self._profile = kwargs.pop('profiler')
        super(ProfileDaemon, self).__init__(*args, **kwargs)

    def handle_message(self, message):
        """Profile code a ship the results."""
        if message.message_type != messages.ProfileRequest.message_type:

            self._error.send(
                messages.ProfileFailure(
                    identifier=message.identifier,
                    setup=None,
                    code=None,
                    message='Invalid profile request.',
                ),
            )
            self._source.complete(message)
            return None

        try:

            value, unit = self._profile(
                setup=message.setup or 'pass',
                code=message.code or 'pass',
            )

        except Exception as exc:

            self._error.send(
                messages.ProfileFailure(
                    identifier=message.identifier,
                    setup=message.setup,
                    code=message.code,
                    message=str(exc),
                ),
            )
            self._source.complete(message)
            return None

        self._results.send(
            message.ProfileResult(
                identifier=message.identifier,
                setup=message.setup,
                code=message.code,
                value=value,
                unit=unit,
            ),
        )
        self._source.complete(message)
        return None
