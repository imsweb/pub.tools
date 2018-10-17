import unittest
from datetime import datetime

from .. import cooking
from ..citations import (
    book_citation, chapter_citation, conference_citation, journal_citation, monograph_citation, period, punctuate,
    report_citation)
from ..config import NO_VALUE


class TestCooking(unittest.TestCase):
    def test_citation_basics(self):
        start = ''
        expected = ''
        self.assertEqual(punctuate(start, ''), expected)
        start = 'foo'
        expected = 'foo.'
        self.assertEqual(punctuate(start, '.'), expected)
        start = 'foo+'
        expected = 'foo+'
        self.assertEqual(punctuate(start, '+'), expected)
        start = 'foo'
        expected = 'foo. '
        self.assertEqual(period(start), expected)
        start = 'foo.'
        expected = 'foo. '
        self.assertEqual(period(start), expected)

    def test_journal_citation(self):
        record = {
            'title': 'My title',
            'authors': [{'lname': 'Wohnlich', 'iname': 'E'}, {'lname': 'Carter', 'iname': 'G'}],
            'journal': 'Sample Journal',
            'pubdate': 'Jan 2007',
            'volume': '4',
            'issue': '5',
            'pagination': '345-7',
            'pubmodel': 'Print',
            'italicize': True,
        }
        citation = 'Wohnlich E, Carter G. My title. <i>Sample Journal</i> Jan 2007;4(5):345-7.'
        self.assertEqual(citation, journal_citation(**record))

        record['issue'] = ''
        citation = 'Wohnlich E, Carter G. My title. <i>Sample Journal</i> Jan 2007;4:345-7.'
        self.assertEqual(citation, journal_citation(**record))

        record['issue'] = '5'
        record['volume'] = ''
        citation = 'Wohnlich E, Carter G. My title. <i>Sample Journal</i> Jan 2007;(5):345-7.'
        self.assertEqual(citation, journal_citation(**record))

        record['pagination'] = ''
        citation = 'Wohnlich E, Carter G. My title. <i>Sample Journal</i> Jan 2007;(5).'
        self.assertEqual(citation, journal_citation(**record))

        record['journal'] = ''
        citation = 'Wohnlich E, Carter G. My title. Jan 2007;(5).'
        self.assertEqual(citation, journal_citation(**record))

    def test_journal_abstract_citation(self):
        record = {
            'title': 'My title',
            'authors': [{'lname': 'Wohnlich', 'iname': 'E'}, {'lname': 'Carter', 'iname': 'G'}],
            'journal': 'Sample Journal',
            'pubdate': 'Jan 2007',
            'volume': '4',
            'issue': '5',
            'pagination': '345-7',
            'pubmodel': 'Print',
            'abstract': [{'label': 'INTRO', 'text': 'my findings'}],
            'use_abstract': True
        }
        citation = '<b>Author: </b>Wohnlich E, Carter G<br/><b>Title: </b>My title<br/><b>Journal: ' \
                   '</b>Sample Journal. 4(5):345-7<br/><b>Pubmed link: </b>' \
                   '<a href="http://www.ncbi.nlm.nih.gov/pubmed/">http://www.ncbi.nlm.nih.gov/pubmed/</a>' \
                   '<br/><b>Citation Date: </b>Jan 2007<br/><b>Abstract: </b>INTRO: my findings<br/>'
        self.assertEqual(citation, journal_citation(**record))

    def test_book_citation(self):
        record = {
            'title': 'My title',
            'authors': ({'lname': 'Wohnlich', 'iname': 'E'}, {'lname': 'Carter', 'iname': 'G'},),
            'editors': ({'lname': 'Van Halen', 'iname': 'E'},),
            'edition': 'First Edition',
            'pubdate': '2007 Dec',
            'publisher': 'Doubleday',
            'pubplace': 'New York',
            'pagination': '243',
            'series': 'My series',
        }
        citation = 'Wohnlich E, Carter G. My title. First Edition. Van Halen E, editor. New York: ' \
                   'Doubleday; 2007 Dec. p. 243. (My series)'
        self.assertEqual(citation, book_citation(**record))

        record['pubdate'] = ''
        citation = 'Wohnlich E, Carter G. My title. First Edition. Van Halen E, editor. New York: ' \
                   'Doubleday. p. 243. (My series)'
        self.assertEqual(citation, book_citation(**record))

        record['publisher'] = ''
        citation = 'Wohnlich E, Carter G. My title. First Edition. Van Halen E, editor. New York. ' \
                   'p. 243. (My series)'
        self.assertEqual(citation, book_citation(**record))

        record['authors'] = []
        citation = 'Van Halen E, editor. My title. First Edition. New York. p. 243. (My series)'
        self.assertEqual(citation, book_citation(**record))

    def test_chapter_citation(self):
        record = {
            'title': 'My title',
            'booktitle': 'My Book',
            'authors': ({'lname': 'Wohnlich', 'iname': 'E'}, {'lname': 'Carter', 'iname': 'G'},),
            'editors': ({'lname': 'Van Halen', 'iname': 'E'},),
            'edition': 'First Edition',
            'pubdate': '2007 Dec',
            'publisher': 'Doubleday',
            'pubplace': 'New York',
            'pagination': '243',
            'series': 'My series',
        }
        citation = 'Wohnlich E, Carter G. My title. In: Van Halen E, editor. My Book. First Edition. ' \
                   'New York: Doubleday; 2007 Dec. p. 243. (My series)'
        self.assertEqual(citation, chapter_citation(**record))

        record['pubdate'] = ''
        citation = 'Wohnlich E, Carter G. My title. In: Van Halen E, editor. My Book. First Edition. ' \
                   'New York: Doubleday. p. 243. (My series)'
        self.assertEqual(citation, chapter_citation(**record))

        record['publisher'] = ''
        citation = 'Wohnlich E, Carter G. My title. In: Van Halen E, editor. My Book. First Edition. ' \
                   'New York. p. 243. (My series)'
        self.assertEqual(citation, chapter_citation(**record))

        record['authors'] = []
        citation = 'Van Halen E, editor. My title. In: My Book. First Edition. New York. p. 243. (My series)'
        self.assertEqual(citation, chapter_citation(**record))

    def test_conference_citation(self):
        record = {
            'title': 'My title',
            'booktitle': 'My Book',
            'authors': ({'lname': 'Wohnlich', 'iname': 'E'}, {'lname': 'Battle', 'iname': 'J'},),
            'editors': ({'lname': 'Sagan', 'iname': 'C'}, {'lname': 'Thorne', 'iname': 'K'}),
            'conferencename': 'Conference name',
            'conferencedate': '2007 Dec',
            'place': 'New York',
            'pubdate': '2008 Jan',
            'publisher': 'Doubleday',
            'pubplace': 'Boston',
            'pagination': '345',
            'italicize': True,
        }
        citation = 'Wohnlich E, Battle J. My title. Sagan C, Thorne K, editors. <i>Proceedings of Conference name' \
                   '</i>; 2007 Dec; New York. Boston: Doubleday; 2008 Jan. p. 345.'
        self.assertEqual(citation, conference_citation(**record))

        record['authors'] = []
        citation = 'Sagan C, Thorne K, editors. My title. <i>Proceedings of Conference name</i>; 2007 Dec; New ' \
                   'York. Boston: Doubleday; 2008 Jan. p. 345.'
        self.assertEqual(citation, conference_citation(**record))

        record['authors'] = ({'lname': 'Wohnlich', 'iname': 'E'}, {'lname': 'Battle', 'iname': 'J'},)
        record['pagination'] = ''
        citation = 'Wohnlich E, Battle J. My title. Sagan C, Thorne K, editors. <i>Proceedings of Conference ' \
                   'name</i>; 2007 Dec; New York. Boston: Doubleday; 2008 Jan.'
        self.assertEqual(citation, conference_citation(**record))

        record['publisher'] = ''
        citation = 'Wohnlich E, Battle J. My title. Sagan C, Thorne K, editors. <i>Proceedings of Conference ' \
                   'name</i>; 2007 Dec; New York. Boston: 2008 Jan.'
        self.assertEqual(citation, conference_citation(**record))

        record['pubplace'] = ''
        citation = 'Wohnlich E, Battle J. My title. Sagan C, Thorne K, editors. <i>Proceedings of Conference ' \
                   'name</i>; 2007 Dec; New York. 2008 Jan.'
        self.assertEqual(citation, conference_citation(**record))

    def test_monograph_citation(self):
        record = {'title': 'My title',
                  'booktitle': 'My Book',
                  'authors': ({'lname': 'Wohnlich', 'iname': 'E'}, {'lname': 'Battle', 'iname': 'J'},),
                  'serieseditors': ('Hawking S', 'Wheeler J'),
                  'series': 'Series name',
                  'reportnum': '5',
                  'weburl': 'http://plone.org',
                  'pubdate': '2010 Feb',
                  'publisher': 'Doubleday',
                  'pubplace': 'Baltimore', }
        citation = 'Wohnlich E, Battle J; My title. Series name. Hawking S, Wheeler J, editors. Baltimore: ' \
                   'Doubleday; 2010 Feb. 5. Available at http://plone.org.'
        self.assertEqual(citation, monograph_citation(**record))

        record['weburl'] = ''
        citation = 'Wohnlich E, Battle J; My title. Series name. Hawking S, Wheeler J, editors. Baltimore: ' \
                   'Doubleday; 2010 Feb. 5.'
        self.assertEqual(citation, monograph_citation(**record))

        record['authors'] = []
        citation = 'Hawking S, Wheeler J, editors. My title. Series name. Baltimore: Doubleday; 2010 Feb. 5.'
        self.assertEqual(citation, monograph_citation(**record))

        record['authors'] = ({'lname': 'Wohnlich', 'iname': 'E'}, {'lname': 'Battle', 'iname': 'J'},)
        record['title'] = ''
        citation = 'Wohnlich E, Battle J; Series name. Hawking S, Wheeler J, editors. Baltimore: Doubleday; ' \
                   '2010 Feb. 5.'
        self.assertEqual(citation, monograph_citation(**record))

        record['pubplace'] = ''
        citation = 'Wohnlich E, Battle J; Series name. Hawking S, Wheeler J, editors. Doubleday; 2010 Feb. 5.'
        self.assertEqual(citation, monograph_citation(**record))

        record['publisher'] = ''
        citation = 'Wohnlich E, Battle J; Series name. Hawking S, Wheeler J, editors. 2010 Feb. 5.'
        self.assertEqual(citation, monograph_citation(**record))

    def test_report_citation(self):
        record = {'title': 'My title',
                  'booktitle': 'My Book',
                  'authors': ({'lname': 'Wohnlich', 'iname': 'E'}, {'lname': 'Battle', 'iname': 'J'},),
                  'editors': ({'lname': 'Hawking', 'iname': 'S'}, {'lname': 'Wheeler', 'iname': 'J'},),
                  'series': 'Series name',
                  'reportnum': '5',
                  'weburl': 'http://plone.org',
                  'pubdate': '2010 Feb',
                  'publisher': 'Doubleday',
                  'pubplace': 'Baltimore', }
        citation = 'Wohnlich E, Battle J. My title. Series name. Hawking S, Wheeler J, editors. Baltimore: ' \
                   'Doubleday; 2010 Feb. 5. Available at http://plone.org.'
        self.assertEqual(citation, report_citation(**record))

        record['weburl'] = ''
        citation = 'Wohnlich E, Battle J. My title. Series name. Hawking S, Wheeler J, editors. Baltimore: ' \
                   'Doubleday; 2010 Feb. 5.'
        self.assertEqual(citation, report_citation(**record))

        record['authors'] = []
        citation = 'Hawking S, Wheeler J, editors. My title. Series name. Baltimore: Doubleday; 2010 Feb. 5.'
        self.assertEqual(citation, report_citation(**record))

        record['authors'] = ({'lname': 'Wohnlich', 'iname': 'E'}, {'lname': 'Battle', 'iname': 'J'},)
        record['title'] = ''
        citation = 'Wohnlich E, Battle J. Series name. Hawking S, Wheeler J, editors. Baltimore: Doubleday; ' \
                   '2010 Feb. 5.'
        self.assertEqual(citation, report_citation(**record))

        record['pubplace'] = ''
        citation = 'Wohnlich E, Battle J. Series name. Hawking S, Wheeler J, editors. Doubleday; 2010 Feb. 5.'
        self.assertEqual(citation, report_citation(**record))

        record['publisher'] = ''
        citation = 'Wohnlich E, Battle J. Series name. Hawking S, Wheeler J, editors. 2010 Feb. 5.'
        self.assertEqual(citation, report_citation(**record))

    def test_blankify(self):
        preb = ''
        expected = NO_VALUE
        b = cooking.blankify(preb)
        self.assertEqual(b, expected)

    def test_date_slash(self):
        pre = '2010 July/August'
        expected = datetime(2010, 7, 1)
        d = cooking.cook_date(None, None, None, pre)
        self.assertEqual(d, expected)

    def test_date_slash_str(self):
        pre = '2010 July/August'
        expected = '2010 Jul-Aug'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_slash_m_first(self):
        pre = 'July - August 1968'
        expected = '1968 Jul-Aug'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str1(self):
        pre = '8/11/2009'
        expected = '2009 Aug 11'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str2(self):
        pre = '8-11-2009'
        expected = '2009 Aug 11'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str3(self):
        pre = '15/8/2009'
        expected = '2009 Aug 15'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str4(self):
        pre = '2009 Aug 15'
        expected = '2009 Aug 15'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str5(self):
        pre = 'Aug 15 2009'
        expected = '2009 Aug 15'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str6(self):
        pre = '15 Aug 2009'
        expected = '2009 Aug 15'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str7(self):
        pre = '11 Aug 2009'
        expected = '2009 Aug 11'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str8(self):
        pre = 'Aug 15, 2009'
        expected = '2009 Aug 15'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str9(self):
        pre = 'Winter 2008'
        expected = '2008 Winter'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str10(self):
        pre = 'Fall-Winter 2008'
        expected = '2008 Fall-Winter'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str11(self):
        pre = '2009 Dec-2010 Jan'
        expected = '2009 Dec'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str12(self):
        pre = 'Dec 4 2009'
        expected = '2009 Dec 4'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_date_str13(self):
        pre = '2009 Aug 15th'
        expected = '2009 Aug 15'
        d = cooking.cook_date_str(pre)
        self.assertEqual(d, expected)

    def test_datetime1(self):
        pre = '8/11/2009'
        expected = datetime(2009, 11, 8)
        d = cooking.cook_date(None, None, None, pre)
        self.assertEqual(d.year, expected.year)
        self.assertEqual(d.month, expected.month)
        self.assertEqual(d.day, expected.day)

    def test_datetime2(self):
        pre = '8 11 2009'
        expected = datetime(2009, 11, 8)
        d = cooking.cook_date(None, None, None, pre)
        self.assertEqual(d.year, expected.year)
        self.assertEqual(d.month, expected.month)
        self.assertEqual(d.day, expected.day)

    def test_datetime3(self):
        pre = '15/8/2009'
        expected = datetime(2009, 8, 15)
        d = cooking.cook_date(None, None, None, pre)
        self.assertEqual(d.year, expected.year)
        self.assertEqual(d.month, expected.month)
        self.assertEqual(d.day, expected.day)

    def test_datetime4(self):
        pre = '15 Aug 2009'
        expected = datetime(2009, 8, 15)
        d = cooking.cook_date(None, None, None, pre)
        self.assertEqual(d.year, expected.year)
        self.assertEqual(d.month, expected.month)
        self.assertEqual(d.day, expected.day)

    def test_datetime5(self):
        pre = '11 Aug 2009'
        expected = datetime(2009, 8, 11)
        d = cooking.cook_date(None, None, None, pre)
        self.assertEqual(d.year, expected.year)
        self.assertEqual(d.month, expected.month)
        self.assertEqual(d.day, expected.day)

    def test_datetime6(self):
        pre = '15 Aug, 2009'
        expected = datetime(2009, 8, 15)
        d = cooking.cook_date(None, None, None, pre)
        self.assertEqual(d.year, expected.year)
        self.assertEqual(d.month, expected.month)
        self.assertEqual(d.day, expected.day)

    def test_datetime7(self):
        pre = 'Winter 2008'
        expected = datetime(2008, 1, 1)
        d = cooking.cook_date(None, None, None, pre)
        self.assertEqual(d.year, expected.year)
        self.assertEqual(d.month, expected.month)
        self.assertEqual(d.day, expected.day)

    def test_datetime8(self):
        pre = 'Jun 2008'
        expected = datetime(2008, 6, 1)
        d = cooking.cook_date(None, None, None, pre)
        self.assertEqual(d.year, expected.year)
        self.assertEqual(d.month, expected.month)
        self.assertEqual(d.day, expected.day)

    def test_datetime9(self):
        pre = 'Spring-Fall 2008'
        expected = datetime(2008, 4, 1)
        d = cooking.cook_date(None, None, None, pre)
        self.assertEqual(d.year, expected.year)
        self.assertEqual(d.month, expected.month)
        self.assertEqual(d.day, expected.day)

    def test_datetime10(self):
        pre = '2009 Dec-2010 Jan'
        expected = datetime(2009, 12, 1)
        d = cooking.cook_date(None, None, None, pre)
        self.assertEqual(d.year, expected.year)
        self.assertEqual(d.month, expected.month)
        self.assertEqual(d.day, expected.day)

    def test_date_ris1(self):
        pre = '2009 Jun 5'
        expected = '2009/06/05/'
        d = cooking.cook_date_ris(pre)
        self.assertEqual(d, expected)

    def test_date_ris2(self):
        pre = '2009 Spring'
        expected = '2009///Spring'
        d = cooking.cook_date_ris(pre)
        self.assertEqual(d, expected)

    def test_date_ris3(self):
        pre = '18 Apr 1978'
        expected = '1978/04/18/'
        d = cooking.cook_date_ris(pre)
        self.assertEqual(d, expected)

    def test_date_ris4(self):
        # garbage/unknown. What does that 18 mean?
        pre = '18 1980'
        expected = '1980///18'
        d = cooking.cook_date_ris(pre)
        self.assertEqual(d, expected)

    def test_date_ris5(self):
        pre = '1995 Aug 9-16'
        expected = '1995/08/9/'
        d = cooking.cook_date_ris(pre)
        self.assertEqual(d, expected)

    def test_cook_date_end(self):
        pre = '2010 July/August'
        expected = datetime(2010, 8, 1)
        d = cooking.cook_date(None, None, None, pre, end=True)
        self.assertEqual(d, expected)

    def test_date_months(self):
        pre = '2010 July-2011 August'
        expected = ['Jul 2010', 'Aug 2010', 'Sep 2010', 'Oct 2010', 'Nov 2010', 'Dec 2010', 'Jan 2011', 'Feb 2011',
                    'Mar 2011', 'Apr 2011', 'May 2011', 'Jun 2011', 'Jul 2011', 'Aug 2011']
        d = cooking.cook_date_months(start=cooking.cook_date(None, None, None, pre),
                                     end=cooking.cook_date(None, None, None, pre, end=True))
        self.assertEqual(d, expected)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
