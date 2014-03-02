import unittest

from pyperf.profile.basic import BasicPerfSample
from pyperf.profile.interfaces import PerfSampleSet


class TestBasicPerfSample(unittest.TestCase):

    def test_externalize_runs_somewhere_else(self):

        success = True

        def toggle():

            global success
            success = False

        test = BasicPerfSample('', '')
        test._externalize(toggle)
        self.assertTrue(success)

    def test_externalize_reacts_to_exceptions(self):
        """If unhandled, exceptions in externalize hang forever. Catch them."""

        def fail():

            raise Exception()

        test = BasicPerfSample('','')
        with self.assertRaises(Exception):

            test._externalize(fail)

    def test_time_behaves_reasonably(self):
        """Check that obviously longer code is measured as longer running."""

        test1 = BasicPerfSample('for x in range(10): pass')
        test2 = BasicPerfSample('for x in range(10000): pass')

        time1 = test1.time(samples=100)
        time2 = test2.time(samples=100)

        self.assertTrue(time1.runtime < time2.runtime)

    def test_memory_behaves_resonably(self):
        """Check that obviously more consuming code is measured as bigger."""

        test1 = BasicPerfSample('for x in list(range(1)): pass')
        test2 = BasicPerfSample('for x in list(range(10000)): pass')

        mem1 = test1.memory()
        mem2 = test2.memory()

        self.assertTrue(mem1.max < mem2.max)

    def test_profile_runs_both(self):

        test = BasicPerfSample('for x in list(range(10)): pass')
        results = test(samples=100)

        self.assertTrue(results.runtime.runtime > 0)
        self.assertTrue(results.memory.max > 0)

    def test_integrates_with_perf_test_set(self):

        test = PerfSampleSet(
            samples=(
                'for x in list(range(10)): pass',
                'for x in list(range(100)): pass',
                'for x in list(range(10000)): pass',
            ),
            perf_class=BasicPerfSample,
        )

        test.time(samples=100)


if __name__ == '__main__':

    unittest.main()
