import logging
import sys

from sqlalchemy import create_engine

from pyperf.executor.host import HostExecutor
from pyperf.transport.amq import AmqpTransport


AMQP_HOST = 'localhost'
AMQP_USER = 'guest'
AMQP_PASSWORD = 'guest'
AMQP_QUEUE = 'sampleq'

LOG_FILE = '/tmp/host-executor.log'
PID_FILE = '/tmp/host-executor.pid'


engine = create_engine('sqlite:////tmp/perf.db')
transport = AmqpTransport(
    host=AMQP_HOST,
    username=AMQP_USER,
    password=AMQP_PASSWORD,
    queue=AMQP_QUEUE,
)


if __name__ == '__main__':

    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
    d = HostExecutor(
        pidfile=PID_FILE,
        transport=transport,
        engine=engine,
        samples=1,
    )

    action = sys.argv[1]

    if action == "start":

        d.start()

    elif action == "stop":

        d.stop()

    elif action == "restart":

        d.restart()
