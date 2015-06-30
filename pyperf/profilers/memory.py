"""Memory profiler powered by memory_profiler."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import functools

import memory_profiler
import six

from ..interfaces import profiler
from . import base


class BaseMemoryProfiler(base.SubprocessProfiler):

    """Base memory profiler using memory_profiler."""

    aggregate = lambda results: results[-1]

    @property
    def baseline(self):
        results = self.delegate(
            functools.partial(
                memory_profiler.memory_usage,
                (six.exec_, ('pass', globals(), locals()), {}),
            ),
        )
        return sum(results) / len(results)

    def profile(self, setup, code):
        """Execute the code using the timeit profiler."""
        results = memory_profiler.memory_usage(
            (six.exec_, (setup + '\n' + code, globals(), locals()), {}),
        )
        return profiler.ProfileResult(
            value=self.__class__.aggregate(results) - self.baseline,
            unit='megabytes',
        )


class MaxMemoryProfiler(BaseMemoryProfiler):

    """Memory profiler that returns the highest measured memory usage."""

    aggreagate = max


class MinMemoryProfiler(BaseMemoryProfiler):

    """Memory profiler that returns the lowest measured memory usage."""

    aggreagate = min


class AvgMemoryProfiler(BaseMemoryProfiler):

    """Memory profiler that returns the average measured memory usage."""

    aggreagate = lambda results: sum(results) / len(results)
