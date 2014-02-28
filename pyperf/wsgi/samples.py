from ..profile.basic import BasicPerfSample
from ..profile.interfaces import PerfSampleSet

from .store import Store


class SampleCollection(object):

    def on_get(self, req, resp):
        """List all current samples."""

        pass

    def on_post(self, req, resp):
        """Create a new sample."""

        pass


class SampleInstance(object):

    def on_get(self, req, resp, sample_id):
        """Get results of sample."""

        pass


    def on_post(self, req, resp, sample_id):
        """Trigger sample run for new results."""

        results = Store().get(sample_id) or {
            "id": "MISSING",
            "name": "MISSING",
            "setup": "",
            "samples": []
        }

        profiler = PerfSampleSet(
            setup=results['setup'],
            samples=(s['source'] for s in results['samples']),
            perf_class=BasicPerfSample,
        )

        profile = profiler(samples=1)

        new_entry = {
            "id": sample_id,
            "name": results['name'],
            "setup": results['setup'],
            "samples": [
                {
                    "source": s.sample,
                    "runtime": s.runtime.runtime,
                    "memory": s.memory.max,
                }
                for s in profile
            ]
        }

        Store().remove(sample_id)
        Store().add(new_entry)

    on_put = on_post

    def on_delete(self, req, resp, sample_id):
        """Delete the sample."""

        pass
