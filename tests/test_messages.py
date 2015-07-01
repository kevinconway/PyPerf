"""Test suite for message implementations."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json

import pytest

from pyperf import messages


def test_profile_request_json_serializeable():
    """Ensure the ProfileRequest message can be serialized."""
    test_message = messages.ProfileRequest(
        identifier='TEST',
        setup='pass',
        code='pass',
    )
    assert json.dumps(test_message.json) is not None


def test_profile_request_json_round_trip():
    """Ensure the ProfileRequest message can be created from a JSON payload."""
    test_message = messages.ProfileRequest(
        identifier='TEST',
        setup='pass',
        code='pass',
    )
    payload = test_message.json
    round_trip = messages.ProfileRequest.from_json(payload)

    assert test_message.identifier == round_trip.identifier


def test_profile_result_json_serializeable():
    """Ensure the ProfileResult message can be serialized."""
    test_message = messages.ProfileResult(
        identifier='TEST',
        setup='pass',
        code='pass',
        value=1,
        unit='tests',
    )
    assert json.dumps(test_message.json) is not None


def test_profile_result_json_round_trip():
    """Ensure the ProfileResult message can be created from a JSON payload."""
    test_message = messages.ProfileResult(
        identifier='TEST',
        setup='pass',
        code='pass',
        value=1,
        unit='tests',
    )
    payload = test_message.json
    round_trip = messages.ProfileResult.from_json(payload)

    assert test_message.identifier == round_trip.identifier


def test_profile_failure_json_serializeable():
    """Ensure the ProfileFailure message can be serialized."""
    test_message = messages.ProfileFailure(
        identifier='TEST',
        setup='pass',
        code='pass',
        message='TEST FAILURE',
    )
    assert json.dumps(test_message.json) is not None


def test_profile_failure_json_round_trip():
    """Ensure the ProfileFailure message can be created from a JSON payload."""
    test_message = messages.ProfileFailure(
        identifier='TEST',
        setup='pass',
        code='pass',
        message='TEST FAILURE',
    )
    payload = test_message.json
    round_trip = messages.ProfileFailure.from_json(payload)

    assert test_message.identifier == round_trip.identifier


def test_from_json():
    """Ensure the from_json function loads from entry_points."""
    test_message = messages.ProfileRequest(
        identifier='TEST',
        setup='pass',
        code='pass',
    )
    round_trip = messages.from_json(test_message.json)
    assert isinstance(round_trip, messages.ProfileRequest)


def test_from_json_missing_message_type():
    """Ensure the from_json function raises ValueError when missing type."""
    test_message = messages.ProfileRequest(
        identifier='TEST',
        setup='pass',
        code='pass',
    ).json
    test_message.pop('message_type')

    with pytest.raises(ValueError):

        messages.from_json(test_message)


def test_from_json_missing_implementation():
    """Ensure the from_json function raises TypeError when missing impl."""
    test_message = messages.ProfileRequest(
        identifier='TEST',
        setup='pass',
        code='pass',
    ).json
    test_message['message_type'] = 'test_not_found'

    with pytest.raises(TypeError):

        messages.from_json(test_message)
