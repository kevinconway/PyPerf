"Profile implementations using ZeroVM as a sandbox."""

import subprocess
import sys
import tempfile
import timeit

import memory_profiler

from .interfaces import MemoryResults
from .interfaces import Profile
from .interfaces import ProfileSet


class ZvmProfile(Profile):
    """A profiler that uses ZeroVM, timeit, and memory_profiler."""

    def __init__(self, *args, **kwargs):

        self._python = kwargs.pop('python')
        if self._python is None:

            raise ValueError("Must provide a python tar path.")

        super(ZvmProfile, self).__init__(*args, **kwargs)

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

        with tempfile.NamedTemporaryFile() as tmp:

            tmp.write(
                'import timeit\n'
                '\n'
                '\n'
                'SETUP = """{0}"""\n'
                'CODE = """{1}"""\n'
                '\n'
                '\n'
                'print(timeit.timeit(stmt=CODE, setup=SETUP, samples={2}))\n'
                ''.format(self.setup, self.code, samples)
            )
            tmp.flush()

            proc = subprocess.Popen(
                'zvsh --zvm-image="{0}" python @{1}'.format(
                    self._python,
                    tmp.name,
                ),
                stdout=subprocess.PIPE,
                shell=True,
            )
            proc.wait()
            out = proc.stdout.read()

            return float(out)

    def memory(self):
        """Measures the memory usage of the code.

        The value returned is a MemoryResults object containing the
        minimum, average, and maximum memory consumption throughout the run.
        These values may be the same if the code has a short runtime.

        """

        with tempfile.NamedTemporaryFile() as tmp:

            tmp.write(
                '{0}\n'
                '{1}\n'
                ''.format(self.setup, self.code)
            )
            tmp.flush()

            proc = subprocess.Popen(
                'zvsh --zvm-image="{0}" python @{1}'.format(
                    self._python,
                    tmp.name,
                ),
                stdout=subprocess.PIPE,
                shell=True,
            )

            results = memory_profiler.memory_usage(proc)

            return MemoryResults(
                min=min(results),
                avg=sum(results) / len(results),
                max=max(results),
            )
