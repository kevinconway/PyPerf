"""Generic profiler interfaces."""

from collections import namedtuple


TimeResults = namedtuple('TimeResults', ('sample', 'runtime'))

MemoryResults = namedtuple('MemoryResults', ('sample', 'min', 'avg', 'max'))

ProfileResults = namedtuple('ProfileResults', ('sample', 'runtime', 'memory'))


class PerfSample(object):
    """Interface for an individual performance sample that can be run."""

    __slots__ = ('_sample', '_setup')

    def __init__(self, sample, setup=None):
        """Create an instance of a runnable performance sample.

        'sample' is the source code to profile.

        'setup' is an optional block of code to run before the sample that is
        not a part of the measured profile.

        """

        self._sample = sample
        self._setup = setup or 'pass'

    @property
    def sample(self):
        """The Python code that will be profiled."""

        return self._sample

    @property
    def setup(self):
        """The Python code that will be run before the profile."""

        return self._setup

    def time(self, samples=1000000):
        """Measure the runtime of the sample.

        The result is a TimeResults object where the runtime is a floating
        point number representing the number of microseconds the sample took to
        complete. This measure is an average of multiple sample runs.

        'samples' is the number of times the sample should run before averaging
        the results. Samples with a shorter expected runtime should use higher
        values for 'samples'. The default is 1,000,000 which is modeled after
        the default number of samples used by the standard lib timeit module.

        """

        raise NotImplementedError()

    def memory(self):
        """Measures the memory usage of the sample.

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
            sample=self._sample,
            runtime=self.time(samples=samples),
            memory=self.memory(),
        )


class PerfSampleSet(object):
    """Interface for a collection of samples."""

    __slots__ = ('_setup', '_samples', '_perf_class')

    def __init__(self, samples, setup=None, perf_class=None):
        """Create a runnable sample suite.

        'samples' must be an iterable of Python code segments to profile.

        'setup' is an optional segment of code to run before each sample that
        is not profiled.

        'perf_class' is a class that implements the PerfSample interface that
        will be used when generating profiles.

        """

        self._setup = setup or 'pass'
        self._perf_class = perf_class or PerfSample
        self._samples = tuple(
            self._perf_class(sample, self._setup)
            for sample in samples
        )

    @property
    def samples(self):
        """An iterable of Python code segments that will be profiled."""

        return tuple(t.sample for t in self._samples)

    def time(self, samples=1000000):
        """Return an iterable of TimeResults objects."""

        return tuple(sample.time(samples=samples) for sample in self._samples)

    def memory(self):
        """Return an iterable of MemoryResults objects."""

        return tuple(sample.memory() for sample in self._samples)

    def __call__(self, samples=1000000):
        """Return an iterable of ProfileResults objects."""

        return tuple(sample(samples=samples) for sample in self._samples)
