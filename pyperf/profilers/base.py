"""Common bases for all core profiler implementations."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import functools
import multiprocessing

from ..interfaces import profiler


class BaseProfiler(profiler.Profiler):

    """Basic extensible profiler."""

    @staticmethod
    def delegate(func):
        """Delegate code to some other runtime if needed.

        This function resolves to a no-op under this implementation. Subclasses
        may implement additional functionality here if the profile function
        requires a special context to run in.
        """
        return func()

    def profile(self, setup, code):
        """Profile a set of code and return the results.

        This method follows the same signature as the profiler callable
        interface and should implement the actual profiling of code.
        """
        raise NotImplementedError()

    def __call__(self, setup, code):
        """Execute a code profile.

        Args:
            setup (str): The code representing the common setup between this
                profile and other profiles. If may or may not be measured as a
                part of a profile. For example, a CPU profile should most
                likely not measure the setup code but must still execute it.

            code (str): The code to be profiled.

        Returns:
            tuple: The outcome of the profile containing the numeric
                value of the profile and the unit in which the profile is
                measured.
        """
        func = functools.partial(self.profile, setup=setup, code=code)
        functools.update_wrapper(func, self.profile)
        return self.delegate(func)


def pipe_wrapper(func, child):
    """Execute a function and write the results back to a pipe.

    Args:
        func: A callable to execute.
        child (multiprocessing.Pipe): The pipe that will carry the results.

    Retuns:
        tuple: A tuple containing a boolean indicator of whether or not an
            exception occurred and the final output of the function. If no
            exception occurred the value is the return value of the function.
            If an exception occurred the value is the return of sys.exc_info().
    """
    try:

        child.send((False, func()))

    except Exception as exc:

        child.send((True, exc))


def externalize(func):
    """Externalize a function in another process."""
    parent, child = multiprocessing.Pipe()

    @functools.wraps(func)
    def wrapper():
        """Wrap the execution in a subprocess."""
        proc = multiprocessing.Process(target=pipe_wrapper, args=(func, child))
        proc.start()
        excepted, value = parent.recv()
        proc.join()

        if excepted is True:

            raise value

        return value

    return wrapper


class SubprocessProfiler(BaseProfiler):

    """Profiler base that runs profiles in another process space."""

    @staticmethod
    def delegate(func):
        """Externalize the profile in another process."""
        return externalize(func)()
