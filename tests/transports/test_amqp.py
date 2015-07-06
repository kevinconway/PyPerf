"""Integration test suite for the AMQP transport implementation."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json

import amqp
import pytest

from pyperf import messages
from pyperf.transports import amqp as amqptransport


@pytest.fixture(scope='function')
def transport(request):
    """Generate an AMQP transport."""
    return amqptransport.AmqpTransport(
        host=request.config.getoption('--amqp-host'),
        username=request.config.getoption('--amqp-user'),
        password=request.config.getoption('--amqp-password'),
        queue=request.config.getoption('--amqp-queue'),
    )


@pytest.fixture(scope='function')
def channel(request):
    """Generate a raw AMQP channel and test queue name."""
    connection = amqp.Connection(
        host=request.config.getoption('--amqp-host'),
        username=request.config.getoption('--amqp-user'),
        password=request.config.getoption('--amqp-password'),
    )
    queue = request.config.getoption('--amqp-queue')
    chan = connection.channel()
    return chan, queue


@pytest.fixture(scope='function')
def message():
    """Get a basic message for testing."""
    return messages.ProfileRequest(
        identifier='test',
        setup='pass',
        code='pass',
    )


@pytest.mark.amqp
def test_transport_sends_messages(transport, channel, message):
    """Ensure messages sent are placed on the queue."""
    transport.send(message)
    channel, queue = channel
    payload = channel.basic_get(queue)
    assert payload is not None
    channel.basic_ack(payload.delivery_tag)


@pytest.mark.amqp
def test_transport_fetches_messages(transport, channel, message):
    """Ensure messages on the queue are fetch by the transport."""
    channel, queue = channel
    msg = amqp.Message(
        json.dumps(message.json),
        content_type='application/json',
    )
    channel.basic_publish_confirm(msg, routing_key=queue)
    fetched = transport.fetch()
    assert fetched is not None
    assert fetched.message_type == message.message_type
    transport.complete(fetched)
