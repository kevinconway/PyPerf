"""Generic profiler interfaces."""

from collections import namedtuple


ProfileResults = namedtuple(
    'ProfileResults',
    (
        'setup',
        'code',
        'runtime',
        'memory',
    ),
)


MemoryResults = namedtuple(
    'MemoryResults',
    (
        'min',
        'avg',
        'max',
    ),
)


class Profile(object):
    """A profiler for a single snippet of code."""

    __slots__ = ('_code', '_setup')

    def __init__(self, code, setup=None):
        """Create an instance of a runnable profiler.

        'code' is the source code to profile.

        'setup' is an optional block of code to run before the profiled code
        that is not a part of the measured runtime. It may, however, count
        against a memory profile.

        """

        self._code = code
        self._setup = setup or 'pass'

    @property
    def code(self):
        """The Python code that will be profiled."""

        return self._code

    @property
    def setup(self):
        """The Python code that will be run before the profile."""

        return self._setup

    def time(self, samples=1000000):
        """Measure the runtime of the code.

        The result is a floating point number which represents the runtime of
        the code in microseconds. This measure is an average of all runtimes
        collected over all samples.

        'samples' is the number of times the code should run before averaging
        the results. Code with a shorter expected runtime should use higher
        values for 'samples'. The default is 1,000,000 which is modeled after
        the default number of samples used by the standard lib timeit module.

        """

        raise NotImplementedError()

    def memory(self):
        """Measures the memory usage of the code.

        The value returned is a MemoryResults object containing the
        minimum, average, and maximum memory consumption throughout the run.
        These values may be the same if the code has a short runtime.

        """

        raise NotImplementedError()

    def __call__(self, samples=1000000):
        """Measure both memory and runtime performance.

        The value returned is a ProfileResults containing the runtime and
        memory profile values.

        The 'samples' value is proxied to the 'time' method.

        """

        return ProfileResults(
            setup=self._setup,
            code=self._code,
            runtime=self.time(samples=samples),
            memory=self.memory(),
        )


class ProfileSet(object):
    """Interface for a collection of profiles."""

    __slots__ = ('_setup', '_profiles')

    ProfileClass = Profile

    def __init__(self, code, setup=None):
        """Create a runnable profile suite.

        'code' must be an iterable of Python code segments to profile.

        'setup' is an optional segment of code to run before each sample that
        is not profiled.

        """

        self._setup = setup or 'pass'
        self._profiles = tuple(
            self.ProfileClass(c, setup=self._setup)
            for c in code
        )

    @property
    def setup(self):
        """The setup code for each profile."""

        return self._setup

    @property
    def code(self):
        """An iterable of Python code segments that will be profiled."""

        return tuple(p.code for p in self._profiles)

    def time(self, samples=1000000):
        """Return an iterable of time profile results."""

        return tuple(p.time(samples=samples) for p in self._profiles)

    def memory(self):
        """Return an iterable of MemoryResults objects."""

        return tuple(p.memory() for p in self._profiles)

    def __call__(self, samples=1000000):
        """Return an iterable of ProfileResults objects."""

        return tuple(p(samples=samples) for p in self._profiles)
