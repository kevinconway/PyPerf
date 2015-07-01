"""Runtime profiler powered by timeit."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import timeit

import confpy.api

from ..interfaces import profiler
from . import base


class RuntimeProfiler(base.SubprocessProfiler):

    """Profiler for CPU runtime."""

    def __init__(self, times=1000):
        """Initialize the profiler with a number of repetitions."""
        self.times = times

    def profile(self, setup, code):
        """Execute the code using the timeit profiler."""
        return profiler.ProfileResult(
            value=(
                timeit.timeit(setup=setup, stmt=code, number=self.times) /
                self.times
            ),
            unit='seconds',
        )


confpy.api.Configuration(
    runtime=confpy.api.Namespace(
        description="Options for the runtime profiler.",
        times=confpy.api.IntegerOption(
            description="Number of times to run a snippet of code.",
            default=1000,
        )
    ),
)


def runtime_profiler_driver(config):
    """Driver interface for the RuntimeProfiler."""
    return RuntimeProfiler(times=config.runtime.times)
