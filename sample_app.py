from wsgiref import simple_server

from sqlalchemy import create_engine

from pyperf.wsgi.app import make_app


engine = create_engine('sqlite://')
app = make_app(engine)


if __name__ == '__main__':

    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
