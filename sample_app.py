from wsgiref import simple_server

from sqlalchemy import create_engine

from pyperf.transport.amq import AmqpTransport
from pyperf.wsgi.app import make_app


engine = create_engine('sqlite:////tmp/perf.db')
transport = AmqpTransport(
    host='localhost',
    username='guest',
    password='guest',
    queue='sampleq',
)
app = make_app(engine, transport=transport)


if __name__ == '__main__':

    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
