"""Generic profiler interfaces."""

from collections import namedtuple


TimeResults = namedtuple('TimeResults', ('test', 'runtime'))

MemoryResults = namedtuple('MemoryResults', ('test', 'min', 'avg', 'max'))

ProfileResults = namedtuple('ProfileResults', ('test', 'runtime', 'memory'))


class PerfTest(object):
    """Interface for an individual performance test that can be run."""

    __slots__ = ('_test', '_setup')

    def __init__(self, test, setup=None):
        """Create an instance of a runnable performance test.

        'test' is the source code to profile.

        'setup' is an optional block of code to run before the test that is
        not a part of the measured profile.

        """

        self._test = test
        self._setup = setup or 'pass'

    @property
    def test(self):
        """The Python code that will be profiled."""

        return self._test

    @property
    def setup(self):
        """The Python code that will be run before the profile."""

        return self._setup

    def time(self, samples=1000000):
        """Measure the runtime of the test.

        The result is a TimeResults object where the runtime is a floating
        point number representing the number of microseconds the test took to
        complete. This measure is an average of multiple test runs.

        'samples' is the number of times the test should run before averaging
        the results. Tests with a shorter expected runtime should use higher
        values for 'samples'. The default is 1,000,000 which is modeled after
        the default number of samples used by the standard lib timeit module.

        """

        raise NotImplementedError()

    def memory(self):
        """Measures the memory usage of the test.

        The value returned is a MemoryResults containing the minimum, average,
        and maximum memory consumption throughout the run. For short runs
        these values may be the same.

        """

        raise NotImplementedError()

    def __call__(self, samples=1000000):
        """Measure both memory and runtime performance.

        The value returned is a ProfileResults containing the runtime and
        memory profile values.

        The 'samples' value is proxied to the 'time' method.

        """

        return ProfileResults(
            test=self._test,
            runtime=self.time(samples=samples),
            memory=self.memory(),
        )


class PerfTestSet(object):
    """Interface for a collection of tests."""

    __slots__ = ('_setup', '_tests', '_perf_class')

    def __init__(self, tests, setup=None, perf_class=None):
        """Create a runnable test suite.

        'tests' must be an iterable of Python code segments to profile.

        'setup' is an optional segment of code to run before each test that is
        not profiled.

        'perf_class' is a class that implements the PerfTest interface that
        will be used when generating profiles.

        """

        self._setup = setup or 'pass'
        self._perf_class = perf_class or PerfTest
        self._tests = tuple(
            self._perf_class(test, self._setup)
            for test in tests
        )

    @property
    def tests(self):
        """An iterable of Python code segments that will be profiled."""

        return tuple(t.test for t in self._tests)

    def time(self, samples=1000000):
        """Return an iterable of TimeResults objects."""

        return tuple(test.time(samples=samples) for test in self._tests)

    def memory(self):
        """Return an iterable of MemoryResults objects."""

        return tuple(test.memory() for test in self._tests)

    def __call__(self, samples=1000000):
        """Return an iterable of ProfileResults objects."""

        return tuple(test(samples=samples) for test in self._tests)
