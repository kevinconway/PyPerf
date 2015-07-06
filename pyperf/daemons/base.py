"""Base daemon process."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from daemons.daemonize import simple as simple_daemonize
from daemons.interfaces import message
from daemons.pid import simple as simple_pid
from daemons.signal import simple as simple_signal
from daemons.startstop import simple as simple_startstop


class BaseDaemon(
        simple_pid.SimplePidManager,
        simple_signal.SimpleSignalManager,
        simple_daemonize.SimpleDaemonizeManager,
        message.MessageManager,
        simple_startstop.SimpleStartStopStepManager,
):

    """Basic message daemon that feeds off a transport."""

    def __init__(self, *args, **kwargs):
        """Initialize the daemon with a transport."""
        self._source = kwargs.pop('source_transport')
        self._error = kwargs.pop('error_transport')
        self._results = kwargs.pop('results_transport')
        super(BaseDaemon, self).__init__(*args, **kwargs)

    def dispatch(self, message):
        """No-op dispatch for single threaded activity."""
        return self.handle_message(message)

    def get_message(self):
        """Fetch a message from the transport."""
        return self._source.fetch()

    def handle_message(self, message):
        """Process a message from the transport."""
        raise NotImplementedError()
