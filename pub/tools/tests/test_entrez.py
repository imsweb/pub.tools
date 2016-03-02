from datetime import datetime
from pub.tools import entrez
from pub.tools.citations import journal_citation
import unittest


class TestCase(unittest.TestCase):
    """ Test Entrez utility interaction
    """

    def test_investigators(self):
        """ Import a record with a bunch of investigators """
        pmid = '22606070'
        record = entrez.get_publication(pmid)
        investigators = [
            {'cname': 'Collaborative Group on Epidemiological Studies of Ovarian Cancer'},
            {'lname': 'Beral', 'fname': 'V', 'iname': 'V'},
            {'lname': 'Hermon', 'fname': 'C', 'iname': 'C'},
            {'lname': 'Peto', 'fname': 'R', 'iname': 'R'},
            {'lname': 'Reeves', 'fname': 'G', 'iname': 'G'},
            {'lname': 'Brinton', 'fname': 'L', 'iname': 'L'},
            {'lname': 'Marchbanks', 'fname': 'P', 'iname': 'P'},
            {'lname': 'Negri', 'fname': 'E', 'iname': 'E'},
            {'lname': 'Ness', 'fname': 'R', 'iname': 'R'},
            {'lname': 'Peeters', 'fname': 'P H M', 'iname': 'P'},
            {'lname': 'Vessey', 'fname': 'M', 'iname': 'M'},
            {'lname': 'Gapstur', 'fname': 'S M', 'iname': 'S'},
            {'lname': 'Patel', 'fname': 'A V', 'iname': 'A'},
            {'lname': 'Dal Maso', 'fname': 'L', 'iname': 'L'},
            {'lname': 'Talamini', 'fname': 'R', 'iname': 'R'},
            {'lname': 'Chetrit', 'fname': 'A', 'iname': 'A'},
            {'lname': 'Hirsh', 'fname': 'G', 'iname': 'G'},
            {'lname': 'Lubin', 'fname': 'F', 'iname': 'F'},
            {'lname': 'Sadetzki', 'fname': 'S', 'iname': 'S'},
            {'lname': 'Allen', 'fname': 'N', 'iname': 'N'},
            {'lname': 'Beral', 'fname': 'V', 'iname': 'V'},
            {'lname': 'Bull', 'fname': 'D', 'iname': 'D'},
            {'lname': 'Callaghan', 'fname': 'K', 'iname': 'K'},
            {'lname': 'Crossley', 'fname': 'B', 'iname': 'B'},
            {'lname': 'Gaitskell'},
            {'lname': 'Goodill'},
            {'lname': 'Green', 'fname': 'J', 'iname': 'J'},
            {'lname': 'Hermon', 'fname': 'C', 'iname': 'C'},
            {'lname': 'Key', 'fname': 'T', 'iname': 'T'},
            {'lname': 'Moser', 'fname': 'K', 'iname': 'K'},
            {'lname': 'Reeves', 'fname': 'G', 'iname': 'G'},
            {'lname': 'Collins', 'fname': 'R', 'iname': 'R'},
            {'lname': 'Doll', 'fname': 'R', 'iname': 'R'},
            {'lname': 'Peto', 'fname': 'R', 'iname': 'R'},
            {'lname': 'Gonzalez', 'fname': 'C A', 'iname': 'C'},
            {'lname': 'Lee', 'fname': 'N', 'iname': 'N'},
            {'lname': 'Marchbanks', 'fname': 'P', 'iname': 'P'},
            {'lname': 'Ory', 'fname': 'H W', 'iname': 'H'},
            {'lname': 'Peterson', 'fname': 'H B', 'iname': 'H'},
            {'lname': 'Wingo', 'fname': 'P A', 'iname': 'P'},
            {'lname': 'Martin', 'fname': 'N', 'iname': 'N'},
            {'lname': 'Pardthaisong', 'fname': 'T', 'iname': 'T'},
            {'lname': 'Silpisornkosol', 'fname': 'S', 'iname': 'S'},
            {'lname': 'Theetranont', 'fname': 'C', 'iname': 'C'},
            {'lname': 'Boosiri', 'fname': 'B', 'iname': 'B'},
            {'lname': 'Jimakorn', 'fname': 'P', 'iname': 'P'},
            {'lname': 'Virutamasen', 'fname': 'P', 'iname': 'P'},
            {'lname': 'Wongsrichanalai', 'fname': 'C', 'iname': 'C'},
            {'lname': 'Tjonneland', 'fname': 'A', 'iname': 'A'},
            {'lname': 'Titus-Ernstoff', 'fname': 'L', 'iname': 'L'},
            {'lname': 'Byers', 'fname': 'T', 'iname': 'T'},
            {'lname': 'Rohan', 'fname': 'T', 'iname': 'T'},
            {'lname': 'Mosgaard', 'fname': 'B J', 'iname': 'B'},
            {'lname': 'Vessey', 'fname': 'M', 'iname': 'M'},
            {'lname': 'Yeates', 'fname': 'D', 'iname': 'D'},
            {'lname': 'Freudenheim', 'fname': 'J L', 'iname': 'J'},
            {'lname': 'Chang-Claude', 'fname': 'J', 'iname': 'J'},
            {'lname': 'Kaaks', 'fname': 'R', 'iname': 'R'},
            {'lname': 'Anderson', 'fname': 'K E', 'iname': 'K'},
            {'lname': 'Folsom', 'fname': 'A', 'iname': 'A'},
            {'lname': 'Robien', 'fname': 'K', 'iname': 'K'},
            {'lname': 'Rossing', 'fname': 'M A', 'iname': 'M'},
            {'lname': 'Thomas', 'fname': 'D B', 'iname': 'D'},
            {'lname': 'Weiss', 'fname': 'N S', 'iname': 'N'},
            {'lname': 'Riboli', 'fname': 'E', 'iname': 'E'},
            {'lname': 'Clavel-Chapelon', 'fname': 'F', 'iname': 'F'},
            {'lname': 'Cramer', 'fname': 'D', 'iname': 'D'},
            {'lname': 'Hankinson', 'fname': 'S E', 'iname': 'S'},
            {'lname': 'Tworoger', 'fname': 'S S', 'iname': 'SS'},
            {'lname': 'Franceschi', 'fname': 'S', 'iname': 'S'},
            {'lname': 'Negri', 'fname': 'E', 'iname': 'E'},
            {'lname': 'Magnusson', 'fname': 'C', 'iname': 'C'},
            {'lname': 'Riman', 'fname': 'T', 'iname': 'T'},
            {'lname': 'Weiderpass', 'fname': 'E', 'iname': 'E'},
            {'lname': 'Wolk', 'fname': 'A', 'iname': 'A'},
            {'lname': 'Schouten', 'fname': 'L J', 'iname': 'L'},
            {'lname': 'van den Brandt', 'fname': 'P A', 'iname': 'P'},
            {'lname': 'Chantarakul', 'fname': 'N', 'iname': 'N'},
            {'lname': 'Koetsawang', 'fname': 'S', 'iname': 'S'},
            {'lname': 'Rachawat', 'fname': 'D', 'iname': 'D'},
            {'lname': 'Palli', 'fname': 'D', 'iname': 'D'},
            {'lname': 'Black', 'fname': 'A', 'iname': 'A'},
            {'lname': 'Berrington de Gonzalez', 'fname': 'A', 'iname': 'A'},
            {'lname': 'Brinton', 'fname': 'L A', 'iname': 'L'},
            {'lname': 'Freedman', 'fname': 'D M', 'iname': 'D'},
            {'lname': 'Hartge', 'fname': 'P', 'iname': 'P'},
            {'lname': 'Hsing', 'fname': 'A W', 'iname': 'A'},
            {'lname': 'Lacey', 'fname': 'J V', 'iname': 'J', 'suffix': 'Jr'},
            {'lname': 'Hoover', 'fname': 'R N', 'iname': 'R'},
            {'lname': 'Schairer', 'fname': 'C', 'iname': 'C'},
            {'lname': 'Graff-Iversen', 'fname': 'S', 'iname': 'S'},
            {'lname': 'Selmer', 'fname': 'R', 'iname': 'R'},
            {'lname': 'Bain', 'fname': 'C J', 'iname': 'C'},
            {'lname': 'Green', 'fname': 'A C', 'iname': 'A'},
            {'lname': 'Purdie', 'fname': 'D M', 'iname': 'D'},
            {'lname': 'Siskind', 'fname': 'V', 'iname': 'V'},
            {'lname': 'Webb', 'fname': 'P M', 'iname': 'P'},
            {'lname': 'McCann', 'fname': 'S E', 'iname': 'S'},
            {'lname': 'Hannaford', 'fname': 'P', 'iname': 'P'},
            {'lname': 'Kay', 'fname': 'C', 'iname': 'C'},
            {'lname': 'Binns', 'fname': 'C W', 'iname': 'C'},
            {'lname': 'Lee', 'fname': 'A H', 'iname': 'A'},
            {'lname': 'Zhang', 'fname': 'M', 'iname': 'M'},
            {'lname': 'Ness', 'fname': 'R B', 'iname': 'R'},
            {'lname': 'Nasca', 'fname': 'P', 'iname': 'P'},
            {'lname': 'Coogan', 'fname': 'P F', 'iname': 'P'},
            {'lname': 'Palmer', 'fname': 'J R', 'iname': 'J'},
            {'lname': 'Rosenberg', 'fname': 'L', 'iname': 'L'},
            {'lname': 'Kelsey', 'fname': 'J', 'iname': 'J'},
            {'lname': 'Paffenbarger', 'fname': 'R', 'iname': 'R'},
            {'lname': 'Whittemore', 'fname': 'A', 'iname': 'A'},
            {'lname': 'Katsouyanni', 'fname': 'K', 'iname': 'K'},
            {'lname': 'Trichopoulou', 'fname': 'A', 'iname': 'A'},
            {'lname': 'Trichopoulos', 'fname': 'D', 'iname': 'D'},
            {'lname': 'Tzonou', 'fname': 'A', 'iname': 'A'},
            {'lname': 'Dabancens', 'fname': 'A', 'iname': 'A'},
            {'lname': 'Martinez', 'fname': 'L', 'iname': 'L'},
            {'lname': 'Molina', 'fname': 'R', 'iname': 'R'},
            {'lname': 'Salas', 'fname': 'O', 'iname': 'O'},
            {'lname': 'Goodman', 'fname': 'M T', 'iname': 'M'},
            {'lname': 'Lurie', 'fname': 'G', 'iname': 'G'},
            {'lname': 'Carney', 'fname': 'M E', 'iname': 'M'},
            {'lname': 'Wilkens', 'fname': 'L R', 'iname': 'L'},
            {'lname': 'Hartman', 'fname': 'L', 'iname': 'L'},
            {'lname': 'Manjer', 'fname': 'J', 'iname': 'J'},
            {'lname': 'Olsson', 'fname': 'H', 'iname': 'H'},
            {'lname': 'Grisso', 'fname': 'J A', 'iname': 'J'},
            {'lname': 'Morgan', 'fname': 'M', 'iname': 'M'},
            {'lname': 'Wheeler', 'fname': 'J E', 'iname': 'J'},
            {'lname': 'Peeters', 'fname': 'P H M', 'iname': 'P'},
            {'lname': 'Casagrande', 'fname': 'J', 'iname': 'J'},
            {'lname': 'Pike', 'fname': 'M C', 'iname': 'M'},
            {'lname': 'Ross', 'fname': 'R K', 'iname': 'R'},
            {'lname': 'Wu', 'fname': 'A H', 'iname': 'A'},
            {'lname': 'Miller', 'fname': 'A B', 'iname': 'A'},
            {'lname': 'Kumle', 'fname': 'M', 'iname': 'M'},
            {'lname': 'Lund', 'fname': 'E', 'iname': 'E'},
            {'lname': 'McGowan', 'fname': 'L', 'iname': 'L'},
            {'lname': 'Shu', 'fname': 'X O', 'iname': 'X'},
            {'lname': 'Zheng', 'fname': 'W', 'iname': 'W'},
            {'lname': 'Farley', 'fname': 'T M M', 'iname': 'T'},
            {'lname': 'Holck', 'fname': 'S', 'iname': 'S'},
            {'lname': 'Meirik', 'fname': 'O', 'iname': 'O'},
            {'lname': 'Risch', 'fname': 'H A', 'iname': 'H'},
        ]
        for i in investigators:
            if not i.get('cname'):
                i['investigator'] = True
        for received, expected in zip(record['authors'], investigators):
            self.assertEqual(received.get('lname', u''), expected.get('lname', u''))
            self.assertEqual(received.get('iname', u''), expected.get('iname', u''))
            self.assertEqual(received.get('fname', u''), expected.get('fname', u''))
            self.assertEqual(received.get('suffix', u''), expected.get('suffix', u''))
            self.assertEqual(received.get('cname', u''), expected.get('cname', u''))
            self.assertEqual(bool(received.get('investigator')), bool(expected.get('investigator')))

    def checkPubData(self, pub):
        self.assertEqual(pub['title'], 'Use of agricultural pesticides and prostate cancer risk in the Agricultural Health Study cohort.')
        self.assertEqual(pub['medium'], 'Print')
        self.assertEqual(pub.get('doi') or '', '')
        self.assertEqual(pub.get('nihmsid') or '', '')
        self.assertEqual(pub.get('pmc') or '', '')
        expected = ({'lname': u'Alavanja', 'cname': u'', 'iname': u'MC', 'fname': u'Michael C R', 'suffix': u'', 'investigator': u''}, {'lname': u'Samanic', 'cname': u'', 'iname': u'C', 'fname': u'Claudine', 'suffix': u'', 'investigator': u''}, {'lname': u'Dosemeci', 'cname': u'', 'iname': u'M', 'fname': u'Mustafa', 'suffix': u'', 'investigator': u''}, {'lname': u'Lubin', 'cname': u'', 'iname': u'J', 'fname': u'Jay', 'suffix': u'', 'investigator': u''}, {'lname': u'Tarone', 'cname': u'', 'iname': u'R', 'fname': u'Robert', 'suffix': u'', 'investigator': u''}, {'lname': u'Lynch', 'cname': u'', 'iname': u'CF', 'fname': u'Charles F', 'suffix': u'', 'investigator': u''}, {'lname': u'Knott', 'cname': u'', 'iname': u'C', 'fname': u'Charles', 'suffix': u'', 'investigator': u''}, {'lname': u'Thomas', 'cname': u'', 'iname': u'K', 'fname': u'Kent', 'suffix': u'', 'investigator': u''}, {'lname': u'Hoppin', 'cname': u'', 'iname': u'JA', 'fname': u'Jane A', 'suffix': u'', 'investigator': u''}, {'lname': u'Barker', 'cname': u'', 'iname': u'J', 'fname': u'Joseph', 'suffix': u'', 'investigator': u''}, {'lname': u'Coble', 'cname': u'', 'iname': u'J', 'fname': u'Joseph', 'suffix': u'', 'investigator': u''}, {'lname': u'Sandler', 'cname': u'', 'iname': u'DP', 'fname': u'Dale P', 'suffix': u'', 'investigator': u''}, {'lname': u'Blair', 'cname': u'', 'iname': u'A', 'fname': u'Aaron', 'suffix': u'', 'investigator': u''})
        for r, e in zip(pub['authors'], expected):
            self.assertEqual(r.get('lname', ''), e.get('lname', ''))
            self.assertEqual(r.get('fname', ''), e.get('fname', ''))
            self.assertEqual(r.get('iname', ''), e.get('iname', ''))
            self.assertEqual(r.get('cname', ''), e.get('cname', ''))
            self.assertEqual(r.get('suffix', ''), e.get('suffix', ''))
            self.assertEqual(bool(r.get('investigator')), bool(e.get('investigator')))
        self.assertEqual(pub['journal'] or '', 'American journal of epidemiology')
        self.assertEqual(pub['medlineta'] or '', 'Am J Epidemiol')
        self.assertEqual(pub['volume'] or '', '157')
        self.assertEqual(pub['issue'] or '', '9')
        self.assertEqual(pub.get('pii') or '', '')
        self.assertEqual(pub.get('publisher') or '', '')
        if pub.get('pubdate_date'):
            self.assertEqual(pub['pubdate_date'], datetime(2003, 5, 1))
        self.assertEqual(pub['pubdate'], '2003 May 1')
        self.assertEqual(pub.get('pubplace') or '', '')
        self.assertEqual(pub['affiliation'], 'Division of Cancer Epidemiology and Genetics, National Cancer Institute, Rockville, MD 20892, USA. alavanjm@mail.nih.gov')
        self.assertEqual(pub['medlinecountry'], 'United States')
        self.assertEqual(pub['nlmuniqueid'], '7910653',)
        self.assertEqual(pub['medlinestatus'], 'MEDLINE')
        self.assertEqual(pub['pubtypelist'], ['Journal Article'])
        self.assertEqual(pub['mesh'], ['Adult', 'Age Distribution', 'Aged', "Agricultural Workers' Diseases", 'Cohort Studies', 'Humans',
                         'Incidence', 'Iowa', 'Male', 'Middle Aged', 'North Carolina', 'Odds Ratio', 'Pesticides', 'Prostatic Neoplasms',
                         'Surveys and Questionnaires'])
        self.assertEqual(pub['pagination'], '800-14')
        expected = [{'label': '', 'nlmcategory': '', 'text': 'The authors examined the relation between 45 common agricultural pesticides and prostate cancer incidence in a prospective cohort study of 55,332 male pesticide applicators from Iowa and North Carolina with no prior history of prostate cancer. Data were collected by means of self-administered questionnaires completed at enrollment (1993-1997). Cancer incidence was determined through population-based cancer registries from enrollment through December 31, 1999. A prostate cancer standardized incidence ratio was computed for the cohort. Odds ratios were computed for individual pesticides and for pesticide use patterns identified by means of factor analysis. A prostate cancer standardized incidence ratio of 1.14 (95% confidence interval: 1.05, 1.24) was observed for the Agricultural Health Study cohort. Use of chlorinated pesticides among applicators over 50 years of age and methyl bromide use were significantly associated with prostate cancer risk. Several other pesticides showed a significantly increased risk of prostate cancer among study subjects with a family history of prostate cancer but not among those with no family history. Important family history-pesticide interactions were observed.'}]
        for r, e in zip(pub['abstract'], expected):
            self.assertEqual(r.get('text', ''), e.get('text', ''))
            self.assertEqual(r.get('label', ''), e.get('label', ''))
            self.assertEqual(r.get('nlmcategory', ''), e.get('nlmcategory', ''))
        self.assertEqual(pub['grants'] or [], [])
        self.assertEqual(pub['pubstatus'] or '', 'ppublish')

    def test_pubmed_fetch(self):
        """ Take an existing record and use @@pubmed-compare """
        record = entrez.get_publication('12727674')
        self.checkPubData(record)

    def test_grants(self):
        """ Tests stripping out some white text """
        record = entrez.get_publication('18640298')
        self.assertEqual(record['grants'], [{'grantid': u'F32 CA130434-01', 'acronym': 'CA', 'agency': 'NCI NIH HHS'},
                                            {'grantid': u'T32 CA09168-30', 'acronym': 'CA', 'agency': 'NCI NIH HHS'}])

    def test_generateSearchString(self):
        """ biopython will not take non-ascii chars """
        search = entrez.generate_search_string(authors=u'\xe9', title=u'\xe9', journal=u'\xe9', pmid=u'', mesh=u'', gr=u'', ir=u'', affl=u'', doi=u'')
        self.assertEqual(search, u'e[auth]+e[titl]+"e"[jour]')

    def test_validyn(self):
        record = entrez.get_publication('20051087')
        expected = [{'lname': 'Elder', 'cname': '', 'iname': 'JP', 'fname': 'John P', 'suffix': '', 'investigator': False},
                    {'lname': 'Arredondo', 'cname': '', 'iname': 'EM', 'fname': 'Elva M', 'suffix': '', 'investigator': False},
                    {'lname': 'Campbell', 'cname': '', 'iname': 'N', 'fname': 'Nadia', 'suffix': '', 'investigator': False},
                    {'lname': 'Baquero', 'cname': '', 'iname': 'B', 'fname': 'Barbara', 'suffix': '', 'investigator': False},
                    {'lname': 'Duerksen', 'cname': '', 'iname': 'S', 'fname': 'Susan', 'suffix': '', 'investigator': False},
                    {'lname': 'Ayala', 'cname': '', 'iname': 'G', 'fname': 'Guadalupe', 'suffix': '', 'investigator': False},
                    {'lname': 'Crespo', 'cname': '', 'iname': 'NC', 'fname': 'Noe C', 'suffix': '', 'investigator': False},
                    {'lname': 'Slymen', 'cname': '', 'iname': 'D', 'fname': 'Donald', 'suffix': '', 'investigator': False},
                    {'lname': 'McKenzie', 'cname': '', 'iname': 'T', 'fname': 'Thomas', 'suffix': '', 'investigator': False}]
        for r, e in zip(record['authors'], expected):
            self.assertEqual(r.get('lname', ''), e.get('lname', ''))
            self.assertEqual(r.get('fname', ''), e.get('fname', ''))
            self.assertEqual(r.get('iname', ''), e.get('iname', ''))
            self.assertEqual(r.get('cname', ''), e.get('cname', ''))
            self.assertEqual(r.get('suffix', ''), e.get('suffix', ''))
            self.assertEqual(bool(r.get('investigator')), bool(e.get('investigator')))

    def test_print_electronic_pubmodel(self):
        """ Both dates should be stored and the citation reflect it """
        record = entrez.get_publication(pmid='10854512')
        record['journal'] = record['medlineta']
        self.assertEqual(journal_citation(**record), 'Soon MS, Lin OS. Inflammatory fibroid polyp of the duodenum. <i>Surg Endosc</i> 2000 Jan;14(1):86. Epub 1999 Nov 25.')

    def test_electronic_print_pubmodel(self):
        """ Both dates should be stored but use electronic date for citation """
        record = entrez.get_publication(pmid='14729922')
        record['journal'] = record['medlineta']
        self.assertEqual(journal_citation(**record), 'Edgar RC. Local homology recognition and distance measures in linear time using compressed amino acid alphabets. <i>Nucleic Acids Res</i> 2004 Jan 16;32(1):380-5. Print 2004.')

    def test_electronic_ecollection_pubmodel(self):
        """ Both dates should be stored but use electronic date for citation """
        record = entrez.get_publication(pmid='23372575')
        record['journal'] = record['medlineta']
        self.assertEqual(journal_citation(**record), 'Wangari-Talbot J, Chen S. Genetics of melanoma. <i>Front Genet</i> 2013 Jan 25;3:330. doi: 10.3389/fgene.2012.00330. eCollection 2012.')

    def test_book_parse(self):
        """ Be able to parse a book """
        result = entrez.get_publication(pmid='22593940')

        self.assertEqual(result['volume'], '')
        self.assertEqual(result['volumetitle'], '')
        self.assertEqual(result['edition'], '2nd')
        self.assertEqual(result['series'], '')
        self.assertEqual(result['isbn'], '9781439807132')
        self.assertEqual(result['elocation'], [])
        self.assertEqual(result['medium'], '')
        self.assertEqual(result['reportnum'], '')
        self.assertEqual(result['pubdate'], '2011')
        self.assertEqual(result['pmid'], '22593940')
        self.assertEqual(result['sections'], [])
        self.assertEqual(result['publisher'], 'CRC Press/Taylor & Francis')
        self.assertEqual(result['pubplace'], 'Boca Raton (FL)')
        self.assertEqual(result['title'], 'Herbs and Spices in Cancer Prevention and Treatment')
        self.assertEqual(result['booktitle'], 'Herbal Medicine: Biomolecular and Clinical Aspects')
        self.assertEqual(result['type'], 'chapter')
        self.assertEqual(result['abstract'], 'More than 180 spice-derived compounds have been identified and explored for their health benefits (Aggarwal et al. 2008). It is beyond the scope of this chapter to deal with all herbs and spices that may influence the risk of cancer and tumor behavior. Therefore, a decision was made to review those with some of the more impressive biological responses reported in the literature, and a conscious effort was made to provide information about the amount of spices needed to bring about a response and thus their physiological relevance. When possible, recent reviews are included to provide readers with additional insights into the biological response(s) to specific spices and to prevent duplication of the scientific literature. Because there is a separate chapter devoted to curcumin (a bioactive component in turmeric) in this book and there are also several excellent reviews published about curcumin (Patel and Majumdar 2009; Aggarwal 2010; Bar-Sela, Epelbaum, and Schaffer 2010; Epstein, Sanderson, and Macdonald 2010), turmeric is not discussed in this chapter.')
        self.assertEqual(result['bookaccession'], 'NBK92774')
        self.assertEqual(result['language'], 'eng')
        authors = [{'lname': 'Kaefer', 'iname': 'CM', 'fname': 'Christine M.', 'investigator': False},
                   {'lname': 'Milner', 'iname': 'JA', 'fname': 'John A.', 'investigator': False}]
        editors = [{'lname': 'Benzie', 'iname': 'IFF', 'fname': 'Iris F. F.', 'investigator': False},
                   {'lname': 'Wachtel-Galor', 'iname': 'S', 'fname': 'Sissi', 'investigator': False}]
        for e, r in zip(authors, result['authors']):
            for k in set(e.keys()).union(r.keys()):
                self.assertEqual(e.get(k) or '', r.get(k) or '', msg='%s :: Expected: %s; Received: %s' % (k, e.get(k) or '', r.get(k) or ''))
        for e, r in zip(editors, result['editors']):
            for k in set(e.keys()).union(r.keys()):
                self.assertEqual(e.get(k) or '', r.get(k) or '', msg='%s :: Expected: %s; Received: %s' % (k, e.get(k) or '', r.get(k) or ''))

    def test_find_and_fetch(self):
        record = entrez.find_publications(pmid='12727674')
        self.assertEquals(len(record['IdList']), 1)
        record = entrez.get_searched_publications(record['WebEnv'], record['QueryKey'])
        self.checkPubData(record[0])


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
