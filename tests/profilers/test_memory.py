"""Test suite for the memory profiler."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from pyperf.profilers import memory


def test_memory_gives_reasonable_results():
    """Ensure memory is measured within some degree of reason.

    The expectation is that obviously more expensive code is measured as such
    by the profiler.
    """
    profiler = memory.MaxMemoryProfiler()
    small, _ = profiler(setup='pass', code='for x in list(range(100)): pass')
    large, _ = profiler(setup='pass', code='for x in list(range(10000)): pass')
    assert small < large


def test_memory_gives_repeatable_results():
    """Ensure memory measured is not affected by subsequent runs."""
    profiler = memory.MaxMemoryProfiler()
    first, _ = profiler(setup='pass', code='for x in list(range(10000)): pass')
    second, _ = profiler(
        setup='pass',
        code='for x in list(range(10000)): pass',
    )
    third, _ = profiler(setup='pass', code='for x in list(range(10000)): pass')
    assert first - second < .00001
    assert first - third < .00001
