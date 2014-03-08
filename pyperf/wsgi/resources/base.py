class BaseResource(object):

    def __init__(self, Session, transport):

        self.Session = Session
        self.transport = transport
