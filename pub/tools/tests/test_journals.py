from pub.tools.journals import atoj, jtoa, cache
import unittest

class TestJournals(unittest.TestCase):
    def test_atoj(self):
        self.assertEquals(atoj('J Cancer'), 'Journal of Cancer')

    def test_jtoa(self):
        self.assertEquals(jtoa('Journal of Cancer'), 'J Cancer')

    def test_cache(self):
        # just verify it runs, for test coverage
        cache()

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
