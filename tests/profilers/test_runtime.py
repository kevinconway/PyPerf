"""Test suite for the runtime profiler."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from pyperf.profilers import runtime


def test_runtime_gives_reasonable_results():
    """Ensure runtime is measured within some degree of reason.

    The expectation is that obviously longer running code is measured as longer
    running by the profiler.
    """
    profiler = runtime.RuntimeProfiler()
    small, _ = profiler(setup='pass', code='for x in range(100): pass')
    large, _ = profiler(setup='pass', code='for x in range(10000): pass')
    assert small < large
