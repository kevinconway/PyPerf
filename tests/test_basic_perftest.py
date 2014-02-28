import unittest

from pyperf.basic import BasicPerfTest
from pyperf.interfaces import PerfTestSet


class TestBasicPerfTest(unittest.TestCase):

    def test_externalize_runs_somewhere_else(self):

        success = True

        def toggle():

            global success
            success = False

        test = BasicPerfTest('', '')
        test._externalize(toggle)
        self.assertTrue(success)

    def test_externalize_reacts_to_exceptions(self):
        """If unhandled, exceptions in externalize hang forever. Catch them."""

        def fail():

            raise Exception()

        test = BasicPerfTest('','')
        with self.assertRaises(Exception):

            test._externalize(fail)

    def test_time_behaves_reasonably(self):
        """Check that obviously longer code is measured as longer running."""

        test1 = BasicPerfTest('for x in range(10): pass')
        test2 = BasicPerfTest('for x in range(10000): pass')

        time1 = test1.time(samples=100)
        time2 = test2.time(samples=100)

        self.assertTrue(time1.runtime < time2.runtime)

    def test_memory_behaves_resonably(self):
        """Check that obviously more consuming code is measured as bigger."""

        test1 = BasicPerfTest('for x in list(range(1)): pass')
        test2 = BasicPerfTest('for x in list(range(10000)): pass')

        mem1 = test1.memory()
        mem2 = test2.memory()

        self.assertTrue(mem1.max < mem2.max)

    def test_profile_runs_both(self):

        test = BasicPerfTest('for x in list(range(10)): pass')
        results = test(samples=100)

        self.assertTrue(results.runtime.runtime > 0)
        self.assertTrue(results.memory.max > 0)

    def test_integrates_with_perf_test_set(self):

        test = PerfTestSet(
            tests=(
                'for x in list(range(10)): pass',
                'for x in list(range(100)): pass',
                'for x in list(range(10000)): pass',
            ),
            perf_class=BasicPerfTest,
        )

        test.time(samples=100)


if __name__ == '__main__':

    unittest.main()
