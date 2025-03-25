from pub.tools.journals import atoj, jtoa


class TestJournals:
    def test_atoj(self):
        assert atoj("J Cancer") == "Journal of Cancer"

    def test_jtoa(self):
        assert jtoa("Journal of Cancer") == "J Cancer"

    def test_cache(self):
        assert atoj("J Cancer", cache=True) == "Journal of Cancer"
        assert jtoa("Journal of Cancer", cache=True) == "J Cancer"
