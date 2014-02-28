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

        pass

    on_put = on_post

    def on_delete(self, req, resp, sample_id):
        """Delete the sample."""

        pass
