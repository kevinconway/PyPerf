from ..profile.basic import BasicProfile

from .interfaces import Executor


class HostExecutor(Executor):
    """Execute the profile on the host machine directly."""

    def handle_profile_request(self, message):

        profile = BasicProfile(
            setup=message.setup,
            code=message.code,
        )
        results = profile(samples=self._samples)

        return results
