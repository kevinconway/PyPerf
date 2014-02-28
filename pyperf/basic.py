import multiprocessing
import sys
import timeit

import memory_profiler

from .interfaces import MemoryResults
from .interfaces import PerfTest
from .interfaces import TimeResults


def _get_exec():
    """Polyfill for Py2/Py3 'exec' compatibility.

    This solution brought to you by Ned Batchelder:

    http://nedbatchelder.com/
        blog/200910/running_the_same_code_on_python_2x_and_3x.html

    """

    if sys.hexversion > 0x03000000:

        def exec_function(source, filename, global_map):
            """A wrapper around exec()."""

            exec(compile(source, filename, "exec"), global_map)

    else:

        eval(
            compile(
                """def exec_function(source, filename, global_map):
    exec compile(source, filename, "exec") in global_map""",
                "<exec_function>",
                "exec",
            )
        )

    return exec_function


class BasicPerfTest(PerfTest):

    def _externalize(self, func):
        """Run a test in another process and get the result.

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

                child.send((True, str(exc)))

        proc = multiprocessing.Process(target=run_profile, args=(child,))
        proc.start()
        excepted, value = parent.recv()
        proc.join(3)

        if excepted is True:

            raise Exception(value)

        return value

    def time(self, samples=1000000):

        def profile():

            return (timeit.timeit(
                stmt=self.test,
                setup=self.setup,
                number=samples,
            ) / samples * 1000000)

        return TimeResults(
            test=self.test,
            runtime=self._externalize(profile),
        )

    def memory(self):

        _exec = _get_exec()

        def profile():

            def run_test():
                _exec(
                    source=self.setup + '\n' + self.test,
                    filename='None',
                    global_map=globals(),
                )

            profile = memory_profiler.memory_usage(
                run_test
            )

            return(
                min(profile),
                sum(profile) / len(profile),
                max(profile),
            )

        results = self._externalize(profile)

        return MemoryResults(
            test=self.test,
            min=results[0],
            avg=results[1],
            max=results[2],
        )
