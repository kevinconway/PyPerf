"""Profile implementations using standard lib and pure Python libraries."""

import multiprocessing
import sys
import timeit

import memory_profiler

from .interfaces import MemoryResults
from .interfaces import Profile
from .interfaces import ProfileSet


# The exec interface changes between Python version 2 and 3. This is a simple
# shim which adds cross-platform execing.
if sys.version_info.major > 2:

    import builtins
    _exec = getattr(builtins, 'exec')

else:

    def _exec(source, global_map, local_map):

        exec('exec source in global_map, local_map')


class BasicProfile(Profile):
    """A profiler which uses timeit and memory_profiler."""

    __slots__ = ()

    def _externalize(self, func):
        """Run a function in another process and get the result.

        This is to fix a bug related to incorrect memory values.

        Basically, the memory profiler pings the system for the active
        Python process size. This would cause multiple jobs running in the
        same process to share a memory allocation. This made it impossible to
        get valid results when running multiple, consecutive jobs. To
        safeguard, the profile is executed in an external Python process.

        As a note, the timeit runs also affected the memory profile if the
        job allocated memory.

        """

        parent, child = multiprocessing.Pipe()

        def run_profile(child):

            try:

                child.send((False, func()))

            except Exception as exc:

                child.send((True, exc))

        proc = multiprocessing.Process(target=run_profile, args=(child,))
        proc.start()
        excepted, value = parent.recv()
        proc.join(3)

        if excepted is True:

            raise value

        return value

    def time(self, samples=1000000):
        """Get the timeit results."""

        def measure_time():

            return (timeit.timeit(
                stmt=self.code,
                setup=self.setup,
                number=samples,
            ) / samples * 1000000)

        return self._externalize(measure_time)

    def memory(self):
        """Get the memory_profiler results."""

        def measure_memory():

            def run_code():

                _exec(self.setup + '\n' + self.code, globals(), locals())

            results = memory_profiler.memory_usage(
                run_code,
            )

            return(
                min(results),
                sum(results) / len(results),
                max(results),
            )

        results = self._externalize(measure_memory)

        return MemoryResults(
            min=results[0],
            avg=results[1],
            max=results[2],
        )


class BasicProfileSet(ProfileSet):
    """ProfileSet that uses the BasicProfile."""

    ProfileClass = BasicProfile
