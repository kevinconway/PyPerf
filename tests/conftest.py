"""Global test configuration."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest


def _register_amqp_options(parser):
    """Register CLI options for AMQP transport integration tests."""
    parser.addoption(
        "--amqp-host",
        action="store",
        metavar="HOST",
        help="AMQP hostname to use for tests.",
        default='localhost',
    )
    parser.addoption(
        "--amqp-user",
        action="store",
        metavar="USER",
        help="AMQP username to use for tests.",
        default='guest',
    )
    parser.addoption(
        "--amqp-password",
        action="store",
        metavar="PASSWORD",
        help="AMQP password to use for tests.",
        default='guest',
    )
    parser.addoption(
        "--amqp-queue",
        action="store",
        metavar="QUEUE",
        help="AMQP queue to use for tests.",
        default='pyperf-amqp-tests',
    )
    parser.addoption(
        "--amqp",
        action="store_true",
        help="Enable AMQP integration tests.",
        default=False,
    )


def pytest_addoption(parser):
    """Register custom CLI options for tests."""
    _register_amqp_options(parser)


def _register_amqp_configuration(config):
    """Add any configuration options for AMQP transport integration tests."""
    config.addinivalue_line(
        "markers",
        "amqp: Mark test as an AMQP transport integration tests.",
    )


def pytest_configure(config):
    """Add dynamic test configuration."""
    _register_amqp_configuration(config)


def _register_amqp_setup(item):
    """Add any hooks related to AMQP transport integration tests."""
    envmarker = item.get_marker("amqp")
    if envmarker is not None and not item.config.getoption('--amqp'):

        pytest.skip(
            "AMQP integration tests disabled. Use --amqp to enable."
        )


def pytest_runtest_setup(item):
    """Hook logic into test running."""
    _register_amqp_setup(item)
