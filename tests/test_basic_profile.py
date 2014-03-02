import unittest

from pyperf.profile.basic import BasicProfile
from pyperf.profile.basic import BasicProfileSet


class TestBasicProfile(unittest.TestCase):

    def test_externalize_runs_somewhere_else(self):

        success = True

        def toggle():

            # This will only affect the success variable above if the code
            # is executed in the same Python process as the test.
            global success
            success = False

        test = BasicProfile('', '')
        test._externalize(toggle)
        self.assertTrue(success)

    def test_externalize_reacts_to_exceptions(self):
        """If unhandled, exceptions in externalize hang forever. Catch them."""

        def fail():

            raise ValueError()

        test = BasicProfile('','')
        with self.assertRaises(ValueError):

            test._externalize(fail)

    def test_time_behaves_reasonably(self):
        """Check that obviously longer code is measured as longer running."""

        test1 = BasicProfile('for x in range(10): pass')
        test2 = BasicProfile('for x in range(100000): pass')

        time1 = test1.time(samples=1)
        time2 = test2.time(samples=1)

        self.assertTrue(time1 < time2)

    def test_memory_behaves_resonably(self):
        """Check that obviously more consuming code is measured as bigger."""

        test1 = BasicProfile('for x in list(range(1)): pass')
        test2 = BasicProfile('for x in list(range(100000)): pass')

        mem1 = test1.memory()
        mem2 = test2.memory()

        self.assertTrue(mem1.max < mem2.max)

    def test_call_runs_both(self):

        test = BasicProfile('for x in list(range(10)): pass')
        results = test(samples=10)

        self.assertTrue(results.runtime > 0)
        self.assertTrue(results.memory.max > 0)

    def test_can_work_as_a_set(self):

        test = BasicProfileSet(
            code=(
                'for x in list(range(10)): pass',
                'for x in list(range(100)): pass',
                'for x in list(range(10000)): pass',
            ),
        )

        results = test(samples=10)

        self.assertTrue(len(results) == 3)
        for result in results:

            self.assertTrue(result.runtime > 0)
            self.assertTrue(result.memory.max > 0)


if __name__ == '__main__':

    unittest.main()
