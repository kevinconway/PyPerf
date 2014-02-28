import falcon

from .samples import SampleCollection
from .samples import SampleInstance
from .ui import Index
from .ui import InstanceView

app = falcon.API()

app.add_route('/', Index())
app.add_route('/{sample_id}', InstanceView())
app.add_route('/samples', SampleCollection())
app.add_route('/samples/{sample_id}', SampleInstance())
