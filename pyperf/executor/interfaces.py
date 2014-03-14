from daemons.message import MessageDaemon

from sqlalchemy.orm import sessionmaker

from ..models import Result
from ..transport.messages import Message
from ..transport.messages import ProfileRequest


class Executor(MessageDaemon):

    def __init__(self, *args, **kwargs):

        self._transport = kwargs.pop('transport')
        self._samples = kwargs.pop('samples')
        engine = kwargs.pop('engine')
        self._Session = sessionmaker()
        self._Session.configure(bind=engine)

        super(Executor, self).__init__(*args, **kwargs)

    def get_message(self):

        message = self._transport.fetch()

        if message is None:

            return None

        if not isinstance(message, Message):

            try:

                message = self._transport.message_from_payload(message)

            except:

                return None

        return message

    def handle_message(self, message):

        if isinstance(message, ProfileRequest):

            self.update_results(message, self.handle_profile_request(message))

        self._transport.complete(message)

    def update_results(self, message, results):

        session = self._Session()
        query = session.query(Result)
        query = query.filter(Result.snippet_identity == message.identity)
        record = query.first()
        if record is None:

            record = Result(snippet_identity=message.identity)

        record.runtime = results.runtime
        record.avg_memory = results.memory.avg
        record.max_memory = results.memory.max
        record.min_memory = results.memory.min

        session.add(record)
        session.commit()

    def handle_profile_request(self, message):
        """Profile code and return a ProfileResults."""

        raise NotImplementedError()
