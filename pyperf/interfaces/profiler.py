"""Profiler interfaces."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections

ProfileResult = collections.namedtuple('ProfileResult', ('value', 'unit'))


class Profiler(object):

    """Interface for profilers."""

    def __call__(self, setup, code):
        """Execute a code profile.

        A profiler is any Python callable that implements this signature.

        Args:
            setup (str): The code representing the common setup between this
                profile and other profiles. If may or may not be measured as a
                part of a profile. For example, a CPU profile should most
                likely not measure the setup code but must still execute it.

            code (str): The code to be profiled.

        Returns:
            tuple: The outcome of the profile containing the numeric
                value of the profile and the unit in which the profile is
                measured.
        """
        raise NotImplementedError()
