import json


class Message(object):

    def json(self):

        raise NotImplementedError()


class ProfileRequest(Message):

    def __init__(self, setup, code):

        self._setup = setup
        self._code = code

    @property
    def setup(self):

        return self._setup

    @property
    def code(self):

        return self._code

    def json(self):

        return json.dumps(
            {
                "setup": self._setup,
                "code": self._code,
                "type": "profile_request",
            }
        )
