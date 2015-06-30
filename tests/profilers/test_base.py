"""Test suite for the base profilers."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
import os

import pytest

from pyperf.profilers import base


class FakePipe(object):

    """A minimal pipe implementation."""

    def __init__(self):
        """Initialize the pipe with a queue."""
        self.values = collections.deque()

    def send(self, value):
        """Write a value to the queue."""
        self.values.append(value)

    def recv(self):
        """Pop an item from the queue."""
        return self.values.popleft()


@pytest.fixture(scope='function')
def pipe():
    """Generate a fake multiprocessing pipe."""
    return FakePipe()


def test_pipe_wrapper_writes_results(pipe):
    """Ensure the pipe wrapper sends values back upon success."""
    base.pipe_wrapper(lambda: -1, pipe)
    excepted, value = pipe.recv()
    assert excepted is False
    assert value == -1


def test_pipe_wrapper_writes_exceptions(pipe):
    """Ensure the pipe wrapper sends exceptions back upon exception."""
    exc = TypeError("Wrong type.")

    def run_and_raise():
        """Raise a specific test exception."""
        raise exc

    base.pipe_wrapper(run_and_raise, pipe)
    excepted, value = pipe.recv()
    assert excepted is True
    assert value is exc


def test_externalize_uses_another_process():
    """Ensure externalize does not operate within the current process."""
    current = os.getpid()
    other = base.externalize(os.getpid)()
    assert current != other


def test_externalize_reraises_exceptions():
    """Ensure externalize raises any remote exceptions."""
    exc = TypeError("Custom message.")

    def run_and_raise():
        """Raise the test exception."""
        raise exc

    try:

        base.externalize(run_and_raise)()

    except TypeError as remote_exc:

        assert str(exc) == str(remote_exc)
        return None

    pytest.fail("The exception was not reraised.")
