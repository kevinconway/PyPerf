from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('pyperf', 'templates'))

from .store import Store


class Index(object):

    def on_get(self, req, resp):

        values = Store().get_all()
        template = env.get_template('cannon.html')
        resp.set_header('Content-Type', 'text/html')
        resp.body = template.render(samples=values, page_title='PyPerf')


class InstanceView(object):

    def on_get(self, req, resp, sample_id):

        results = Store().get(sample_id)
        resp.set_header('Content-Type', 'text/html')
        template= env.get_template('cannon_instance.html')
        resp.body = template.render(results=results)
