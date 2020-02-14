import pytest
from david.adapters import adapter
from david.typing import message


def test_name():
    message_adapter = adapter.MessageAdapter()
    assert message_adapter.name() == "message"


def test_validate_data():
    message_adapter = adapter.MessageAdapter()
    correct_payload = {"input": {"text": "text"}}
    wrong_payload = {}
    assert message_adapter.validate_data(correct_payload)
    assert not message_adapter.validate_data(wrong_payload)


def test_input():
    message_adapter = adapter.MessageAdapter()
    correct_payload = {"input": {"text": "text"}}
    correct_input_data = message_adapter.input(correct_payload)
    assert type(correct_input_data) is message.Message

    wrong_payload = {}
    with pytest.raises(KeyError):
        message_adapter.input(wrong_payload)

def test_output():
    message_adapter = adapter.MessageAdapter()
    correct_payload = {"input": {"text": "text"}}
    message = message_adapter.input(correct_payload)
    expected_output = {'input': {'text': 'text'}, 'context': {}, 'time': None, 'data': {}, 'output': {'text': None}}

    assert message_adapter.output(message) == expected_output
    with pytest.raises(AttributeError):
        message_adapter.output({})

