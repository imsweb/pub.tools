import dataclasses
import os
import unittest
from datetime import datetime

from .. import entrez
from ..citations import journal_citation
from ..schema import Abstract
from ..schema import Author
from ..schema import Grant
from ..schema import Section
from ..schema import JournalRecord

base_path = os.path.dirname(os.path.realpath(__file__))


class TestCase(unittest.TestCase):
    """ Test Entrez utility interaction
    """

    def compare_author(self, r: Author, e: Author):
        for field in dataclasses.fields(r):
            field = field.name
            if field == 'affiliations':
                continue
            self.assertEqual(getattr(r, field), getattr(e, field))

    def test_investigators(self):
        """ Import a record with a bunch of investigators """
        pmid = '22606070'
        record = entrez.get_publication(pmid)
        investigators = [
            Author(collective_name='Collaborative Group on Epidemiological Studies of Ovarian Cancer', first_name='',
                   last_name='', initial=''),
            Author(last_name='Beral', first_name='V', initial='V'),
            Author(last_name='Hermon', first_name='C', initial='C'),
            Author(last_name='Peto', first_name='R', initial='R'),
            Author(last_name='Reeves', first_name='G', initial='G'),
            Author(last_name='Brinton', first_name='L', initial='L'),
            Author(last_name='Marchbanks', first_name='P', initial='P'),
            Author(last_name='Negri', first_name='E', initial='E'),
            Author(last_name='Ness', first_name='R', initial='R'),
            Author(last_name='Peeters', first_name='P H M', initial='P'),
            Author(last_name='Vessey', first_name='M', initial='M'),
            Author(last_name='Gapstur', first_name='S M', initial='S'),
            Author(last_name='Patel', first_name='A V', initial='A'),
            Author(last_name='Dal Maso', first_name='L', initial='L'),
            Author(last_name='Talamini', first_name='R', initial='R'),
            Author(last_name='Chetrit', first_name='A', initial='A'),
            Author(last_name='Hirsh', first_name='G', initial='G'),
            Author(last_name='Lubin', first_name='F', initial='F'),
            Author(last_name='Sadetzki', first_name='S', initial='S'),
            Author(last_name='Allen', first_name='N', initial='N'),
            Author(last_name='Beral', first_name='V', initial='V'),
            Author(last_name='Bull', first_name='D', initial='D'),
            Author(last_name='Callaghan', first_name='K', initial='K'),
            Author(last_name='Crossley', first_name='B', initial='B'),
            Author(last_name='Gaitskell', first_name='', initial=''),
            Author(last_name='Goodill', first_name='', initial=''),
            Author(last_name='Green', first_name='J', initial='J'),
            Author(last_name='Hermon', first_name='C', initial='C'),
            Author(last_name='Key', first_name='T', initial='T'),
            Author(last_name='Moser', first_name='K', initial='K'),
            Author(last_name='Reeves', first_name='G', initial='G'),
            Author(last_name='Collins', first_name='R', initial='R'),
            Author(last_name='Doll', first_name='R', initial='R'),
            Author(last_name='Peto', first_name='R', initial='R'),
            Author(last_name='Gonzalez', first_name='C A', initial='C'),
            Author(last_name='Lee', first_name='N', initial='N'),
            Author(last_name='Marchbanks', first_name='P', initial='P'),
            Author(last_name='Ory', first_name='H W', initial='H'),
            Author(last_name='Peterson', first_name='H B', initial='H'),
            Author(last_name='Wingo', first_name='P A', initial='P'),
            Author(last_name='Martin', first_name='N', initial='N'),
            Author(last_name='Pardthaisong', first_name='T', initial='T'),
            Author(last_name='Silpisornkosol', first_name='S', initial='S'),
            Author(last_name='Theetranont', first_name='C', initial='C'),
            Author(last_name='Boosiri', first_name='B', initial='B'),
            Author(last_name='Jimakorn', first_name='P', initial='P'),
            Author(last_name='Virutamasen', first_name='P', initial='P'),
            Author(last_name='Wongsrichanalai', first_name='C', initial='C'),
            Author(last_name='Tjonneland', first_name='A', initial='A'),
            Author(last_name='Titus-Ernstoff', first_name='L', initial='L'),
            Author(last_name='Byers', first_name='T', initial='T'),
            Author(last_name='Rohan', first_name='T', initial='T'),
            Author(last_name='Mosgaard', first_name='B J', initial='B'),
            Author(last_name='Vessey', first_name='M', initial='M'),
            Author(last_name='Yeates', first_name='D', initial='D'),
            Author(last_name='Freudenheim', first_name='J L', initial='J'),
            Author(last_name='Chang-Claude', first_name='J', initial='J'),
            Author(last_name='Kaaks', first_name='R', initial='R'),
            Author(last_name='Anderson', first_name='K E', initial='K'),
            Author(last_name='Folsom', first_name='A', initial='A'),
            Author(last_name='Robien', first_name='K', initial='K'),
            Author(last_name='Rossing', first_name='M A', initial='M'),
            Author(last_name='Thomas', first_name='D B', initial='D'),
            Author(last_name='Weiss', first_name='N S', initial='N'),
            Author(last_name='Riboli', first_name='E', initial='E'),
            Author(last_name='Clavel-Chapelon', first_name='F', initial='F'),
            Author(last_name='Cramer', first_name='D', initial='D'),
            Author(last_name='Hankinson', first_name='S E', initial='S'),
            Author(last_name='Tworoger', first_name='S S', initial='SS'),
            Author(last_name='Franceschi', first_name='S', initial='S'),
            Author(last_name='Negri', first_name='E', initial='E'),
            Author(last_name='Magnusson', first_name='C', initial='C'),
            Author(last_name='Riman', first_name='T', initial='T'),
            Author(last_name='Weiderpass', first_name='E', initial='E'),
            Author(last_name='Wolk', first_name='A', initial='A'),
            Author(last_name='Schouten', first_name='L J', initial='L'),
            Author(last_name='van den Brandt', first_name='P A', initial='P'),
            Author(last_name='Chantarakul', first_name='N', initial='N'),
            Author(last_name='Koetsawang', first_name='S', initial='S'),
            Author(last_name='Rachawat', first_name='D', initial='D'),
            Author(last_name='Palli', first_name='D', initial='D'),
            Author(last_name='Black', first_name='A', initial='A'),
            Author(last_name='Berrington de Gonzalez', first_name='A', initial='A'),
            Author(last_name='Brinton', first_name='L A', initial='L'),
            Author(last_name='Freedman', first_name='D M', initial='D'),
            Author(last_name='Hartge', first_name='P', initial='P'),
            Author(last_name='Hsing', first_name='A W', initial='A'),
            Author(last_name='Lacey', first_name='J V', initial='J', suffix='Jr'),
            Author(last_name='Hoover', first_name='R N', initial='R'),
            Author(last_name='Schairer', first_name='C', initial='C'),
            Author(last_name='Graff-Iversen', first_name='S', initial='S'),
            Author(last_name='Selmer', first_name='R', initial='R'),
            Author(last_name='Bain', first_name='C J', initial='C'),
            Author(last_name='Green', first_name='A C', initial='A'),
            Author(last_name='Purdie', first_name='D M', initial='D'),
            Author(last_name='Siskind', first_name='V', initial='V'),
            Author(last_name='Webb', first_name='P M', initial='P'),
            Author(last_name='McCann', first_name='S E', initial='S'),
            Author(last_name='Hannaford', first_name='P', initial='P'),
            Author(last_name='Kay', first_name='C', initial='C'),
            Author(last_name='Binns', first_name='C W', initial='C'),
            Author(last_name='Lee', first_name='A H', initial='A'),
            Author(last_name='Zhang', first_name='M', initial='M'),
            Author(last_name='Ness', first_name='R B', initial='R'),
            Author(last_name='Nasca', first_name='P', initial='P'),
            Author(last_name='Coogan', first_name='P F', initial='P'),
            Author(last_name='Palmer', first_name='J R', initial='J'),
            Author(last_name='Rosenberg', first_name='L', initial='L'),
            Author(last_name='Kelsey', first_name='J', initial='J'),
            Author(last_name='Paffenbarger', first_name='R', initial='R'),
            Author(last_name='Whittemore', first_name='A', initial='A'),
            Author(last_name='Katsouyanni', first_name='K', initial='K'),
            Author(last_name='Trichopoulou', first_name='A', initial='A'),
            Author(last_name='Trichopoulos', first_name='D', initial='D'),
            Author(last_name='Tzonou', first_name='A', initial='A'),
            Author(last_name='Dabancens', first_name='A', initial='A'),
            Author(last_name='Martinez', first_name='L', initial='L'),
            Author(last_name='Molina', first_name='R', initial='R'),
            Author(last_name='Salas', first_name='O', initial='O'),
            Author(last_name='Goodman', first_name='M T', initial='M'),
            Author(last_name='Lurie', first_name='G', initial='G'),
            Author(last_name='Carney', first_name='M E', initial='M'),
            Author(last_name='Wilkens', first_name='L R', initial='L'),
            Author(last_name='Hartman', first_name='L', initial='L'),
            Author(last_name='Manjer', first_name='J', initial='J'),
            Author(last_name='Olsson', first_name='H', initial='H'),
            Author(last_name='Grisso', first_name='J A', initial='J'),
            Author(last_name='Morgan', first_name='M', initial='M'),
            Author(last_name='Wheeler', first_name='J E', initial='J'),
            Author(last_name='Peeters', first_name='P H M', initial='P'),
            Author(last_name='Casagrande', first_name='J', initial='J'),
            Author(last_name='Pike', first_name='M C', initial='M'),
            Author(last_name='Ross', first_name='R K', initial='R'),
            Author(last_name='Wu', first_name='A H', initial='A'),
            Author(last_name='Miller', first_name='A B', initial='A'),
            Author(last_name='Kumle', first_name='M', initial='M'),
            Author(last_name='Lund', first_name='E', initial='E'),
            Author(last_name='McGowan', first_name='L', initial='L'),
            Author(last_name='Shu', first_name='X O', initial='X'),
            Author(last_name='Zheng', first_name='W', initial='W'),
            Author(last_name='Farley', first_name='T M M', initial='T'),
            Author(last_name='Holck', first_name='S', initial='S'),
            Author(last_name='Meirik', first_name='O', initial='O'),
            Author(last_name='Risch', first_name='H A', initial='H'),
        ]
        for i in investigators:
            if not i.cname:
                i.investigator = True
        for received, expected in zip(record['authors'], investigators):
            self.assertEqual(received, expected)

    def check_pub_data(self, pub: JournalRecord):
        self.assertEqual(pub.title, 'Use of agricultural pesticides and prostate cancer risk in the '
                                    'Agricultural Health Study cohort.')
        self.assertEqual(pub.medium, 'Print')
        self.assertEqual(pub.doi, '10.1093/aje/kwg040')
        self.assertEqual(pub.pmc, None)
        expected = (
            Author(
                last_name='Alavanja',
                first_name='Michael C R',
                initial='MC'
            ),
            Author(
                last_name='Samanic',
                first_name='Claudine',
                initial='C'
            ),
            Author(
                last_name='Dosemeci',
                first_name='Mustafa',
                initial='M'
            ),
            Author(
                last_name='Lubin',
                first_name='Jay',
                initial='J'
            ),
            Author(
                last_name='Tarone',
                first_name='Robert',
                initial='R'
            ),
            Author(
                last_name='Lynch',
                first_name='Charles F',
                initial='CF'
            ),
            Author(
                last_name='Knott',
                first_name='Charles',
                initial='C'
            ),
            Author(
                last_name='Thomas',
                first_name='Kent',
                initial='K'
            ),
            Author(
                last_name='Hoppin',
                first_name='Jane A',
                initial='JA'
            ),
            Author(
                last_name='Barker',
                first_name='Joseph',
                initial='J'
            ),
            Author(
                last_name='Coble',
                first_name='Joseph',
                initial='J'
            ),
            Author(
                last_name='Sandler',
                first_name='Dale P',
                initial='DP'
            ),
            Author(
                last_name='Blair',
                first_name='Aaron',
                initial='A'
            ),
        )
        for r, e in zip(pub.authors, expected):
            # we didn't enter affiliations, it won't match
            self.compare_author(r, e)
        self.assertEqual(pub.journal, 'American journal of epidemiology')
        self.assertEqual(pub.medlineta, 'Am J Epidemiol')
        self.assertEqual(pub.volume, '157')
        self.assertEqual(pub.issue, '9')
        self.assertEqual(pub.pubdate, '2003 May 1')
        self.assertEqual(pub.medlinecountry, 'United States')
        self.assertEqual(pub.nlmuniqueid, '7910653')
        self.assertEqual(pub.medlinestatus, 'MEDLINE')
        self.assertEqual(pub.pubtypelist, ['Journal Article'])
        self.assertEqual(pub.mesh,
                         ['Adult', 'Age Distribution', 'Aged', "Agricultural Workers' Diseases", 'Cohort Studies',
                          'Humans',
                          'Incidence', 'Iowa', 'Male', 'Middle Aged', 'North Carolina', 'Odds Ratio', 'Pesticides',
                          'Prostatic Neoplasms',
                          'Surveys and Questionnaires'])
        self.assertEqual(pub.pagination, '800-14')
        expected = [Abstract(
            label='',
            nlmcategory='',
            text='The authors examined the relation between 45 common agricultural pesticides and prostate '
                 'cancer incidence in a prospective cohort study of 55,332 male pesticide applicators from '
                 'Iowa and North Carolina with no prior history of prostate cancer. Data were collected by '
                 'means of self-administered questionnaires completed at enrollment (1993-1997). Cancer incidence '
                 'was determined through population-based cancer registries from enrollment through December 31, '
                 '1999. A prostate cancer standardized incidence ratio was computed for the cohort. Odds ratios '
                 'were computed for individual pesticides and for pesticide use patterns identified by means of '
                 'factor analysis. A prostate cancer standardized incidence ratio of 1.14 (95% confidence '
                 'interval: 1.05, 1.24) was observed for the Agricultural Health Study cohort. Use of chlorinated '
                 'pesticides among applicators over 50 years of age and methyl bromide use were significantly '
                 'associated with prostate cancer risk. Several other pesticides showed a significantly increased '
                 'risk of prostate cancer among study subjects with a family history of prostate cancer but not '
                 'among those with no family history. Important family history-pesticide interactions were '
                 'observed.'
        )]
        for r, e in zip(pub.abstract, expected):
            try:
                self.assertEqual(r, e)
            except:
                import pdb;
                pdb.set_trace()
        self.assertEqual(pub.grants, [])
        self.assertEqual(pub.pubstatus, 'ppublish')

    def test_pubmed_fetch(self):
        """ Take an existing record and use @@pubmed-compare """
        record = entrez.get_publication('12727674')
        self.check_pub_data(record)

    def test_grants(self):
        """ Tests stripping out some white text """
        record = entrez.get_publication('18640298')
        self.assertEqual(record['grants'], [
            Grant(
                grantid='F32 CA130434-01',
                acronym='CA',
                agency='NCI NIH HHS'),
            Grant(
                grantid='T32 CA09168-30',
                acronym='CA',
                agency='NCI NIH HHS')
        ])

    def test_generate_search_string(self):
        """ biopython will not take non-ascii chars """
        search = entrez.generate_search_string(authors=['\xe9'], title='\xe9', journal='\xe9', pmid='', mesh='',
                                               gr='', ir='', affl='', doi='')
        self.assertEqual(search, 'e[au]+e[ti]+"e"[jour]')

    def test_pmc_search(self):
        """ Get the PMID from PMC"""
        self.assertEqual(entrez.get_pmid_by_pmc('4909985'), '27291797')
        self.assertEqual(entrez.get_pmid_by_pmc('PMC4909985'), '27291797')

    def test_validyn(self):
        record = entrez.get_publication('20051087')
        expected = [
            Author(last_name='Elder', collective_name='', initial='JP', first_name='John P', suffix='',
                   investigator=False),
            Author(last_name='Arredondo', collective_name='', initial='EM', first_name='Elva M', suffix='',
                   investigator=False),
            Author(last_name='Campbell', collective_name='', initial='N', first_name='Nadia', suffix='',
                   investigator=False),
            Author(last_name='Baquero', collective_name='', initial='B', first_name='Barbara', suffix='',
                   investigator=False),
            Author(last_name='Duerksen', collective_name='', initial='S', first_name='Susan', suffix='',
                   investigator=False),
            Author(last_name='Ayala', collective_name='', initial='G', first_name='Guadalupe', suffix='',
                   investigator=False),
            Author(last_name='Crespo', collective_name='', initial='NC', first_name='Noe C', suffix='',
                   investigator=False),
            Author(last_name='Slymen', collective_name='', initial='D', first_name='Donald', suffix='',
                   investigator=False),
            Author(last_name='McKenzie', collective_name='', initial='T', first_name='Thomas', suffix='',
                   investigator=False),
        ]
        for r, e in zip(record['authors'], expected):
            # we didn't enter affiliations, it won't match
            self.compare_author(r, e)

    def test_print_electronic_pubmodel(self):
        """ Both dates should be stored and the citation reflect it """
        record = entrez.get_publication(pmid='10854512')
        self.assertEqual(journal_citation(html=True, publication=record),
                         '<span>Soon MS, Lin OS. Inflammatory fibroid polyp of the duodenum. <i>Surg Endosc</i> 2000 '
                         'Jan;14(1):86. Epub 1999 Nov 25.</span>')

    def test_electronic_print_pubmodel(self):
        """ Both dates should be stored but use electronic date for citation """
        record = entrez.get_publication(pmid='14729922')
        self.assertEqual(journal_citation(html=True, publication=record),
                         '<span>Edgar RC. Local homology recognition and distance measures in linear time using '
                         'compressed '
                         'amino acid alphabets. <i>Nucleic Acids Res</i> 2004 Jan 16;32(1):380-5. Print 2004.</span>')

    def test_electronic_ecollection_pubmodel(self):
        """ Both dates should be stored but use electronic date for citation """
        record = entrez.get_publication(pmid='23372575')
        self.assertEqual(journal_citation(html=True, publication=record),
                         '<span>Wangari-Talbot J, Chen S. Genetics of melanoma. <i>Front Genet</i> 2013 '
                         'Jan 25;3:330. doi: '
                         '10.3389/fgene.2012.00330. eCollection 2012.</span>')

    def test_book_parse(self):
        """ Be able to parse a book """
        result = entrez.get_publication(pmid='22593940')

        self.assertEqual(result.volume, '')
        self.assertEqual(result.volumetitle, '')
        self.assertEqual(result.edition, '2nd')
        self.assertEqual(result.series, '')
        self.assertEqual(result.isbn, '9781439807132')
        self.assertEqual(result.elocation, [])
        self.assertEqual(result.medium, '')
        self.assertEqual(result.reportnum, '')
        self.assertEqual(result.pubdate, '2011')
        self.assertEqual(result.pmid, '22593940')
        self.assertEqual(result.sections, [
            Section(title='INTRODUCTION', section_type='section', label='17.1'),
            Section(title='ALLSPICE', label='17.2', section_type='section'),
            Section(title='BASIL', section_type='section', label='17.3'),
            Section(title='CARAWAY', section_type='section', label='17.4'),
            Section(title='CARDAMOM', section_type='section', label='17.5'),
            Section(title='CINNAMON', section_type='section', label='17.6'),
            Section(title='CLOVE', section_type='section', label='17.7'),
            Section(title='CORIANDER', section_type='section', label='17.8'),
            Section(title='CUMIN', section_type='section', label='17.9'),
            Section(title='DILL', section_type='section', label='17.10'),
            Section(title='GARLIC', section_type='section', label='17.11'),
            Section(title='GINGER', section_type='section', label='17.12'),
            Section(title='ROSEMARY', section_type='section', label='17.13'),
            Section(title='SAFFRON', section_type='section', label='17.14'),
            Section(title='THYME', section_type='section', label='17.15'),
            Section(title='CONCLUSION', section_type='section', label='17.16'),
            Section(title='REFERENCES', section_type='', label=''),
        ])
        self.assertEqual(result.publisher, 'CRC Press/Taylor & Francis')
        self.assertEqual(result.pubplace, 'Boca Raton (FL)')
        self.assertEqual(result.title, 'Herbs and Spices in Cancer Prevention and Treatment')
        self.assertEqual(result.booktitle, 'Herbal Medicine: Biomolecular and Clinical Aspects')
        self.assertEqual(result.type, 'chapter')
        self.assertEqual(result.abstract,
                         'More than 180 spice-derived compounds have been identified and explored for their '
                         'health benefits (Aggarwal et al. 2008). It is beyond the scope of this chapter to '
                         'deal with all herbs and spices that may influence the risk of cancer and tumor '
                         'behavior. Therefore, a decision was made to review those with some of the more '
                         'impressive biological responses reported in the literature, and a conscious effort '
                         'was made to provide information about the amount of spices needed to bring about a '
                         'response and thus their physiological relevance. When possible, recent reviews are '
                         'included to provide readers with additional insights into the biological response(s) '
                         'to specific spices and to prevent duplication of the scientific literature. Because '
                         'there is a separate chapter devoted to curcumin (a bioactive component in turmeric) '
                         'in this book and there are also several excellent reviews published about curcumin '
                         '(Patel and Majumdar 2009; Aggarwal 2010; Bar-Sela, Epelbaum, and Schaffer 2010; '
                         'Epstein, Sanderson, and Macdonald 2010), turmeric is not discussed in this chapter.')
        self.assertEqual(result.language, 'eng')
        authors = [{'lname': 'Kaefer', 'iname': 'CM', 'fname': 'Christine M.', 'investigator': False},
                   {'lname': 'Milner', 'iname': 'JA', 'fname': 'John A.', 'investigator': False}]
        editors = [{'lname': 'Benzie', 'iname': 'IFF', 'fname': 'Iris F. F.', 'investigator': False},
                   {'lname': 'Wachtel-Galor', 'iname': 'S', 'fname': 'Sissi', 'investigator': False}]
        for e, r in zip(authors, result.authors):
            self.assertEqual(e, r)
        for e, r in zip(editors, result.editors):
            self.assertEqual(e, r)

    def test_find_and_fetch(self):
        record = entrez.find_publications(pmid='12727674')
        self.assertEqual(len(record['IdList']), 1)
        record = entrez.get_searched_publications(record['WebEnv'], record['QueryKey'])
        self.check_pub_data(record[0])


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
