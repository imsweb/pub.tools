import dataclasses

from Bio import Entrez

from pub.tools import citations
from pub.tools import entrez
from pub.tools import orcid
from pub.tools.schema import Abstract
from pub.tools.schema import Grant
from pub.tools.schema import JournalRecord
from pub.tools.schema import Person
from pub.tools.schema import Section

Entrez.email = "wohnlice@imsweb.com"


class TestEntrez:
    """Test Entrez utility interaction"""

    def compare_author(self, r: Person, e: Person):
        for field in dataclasses.fields(r):
            field = field.name
            if field == "affiliations":
                continue
            assert getattr(r, field) == getattr(e, field)

    def test_investigators(self):
        """Import a record with a bunch of investigators"""
        pmid = "22606070"
        record = entrez.get_publication(pmid)
        investigators = [
            Person(
                collective_name="Collaborative Group on Epidemiological Studies of Ovarian Cancer",
                first_name="",
                last_name="",
                initial="",
            ),
            Person(last_name="Beral", first_name="V", initial="V"),
            Person(last_name="Hermon", first_name="C", initial="C"),
            Person(last_name="Peto", first_name="R", initial="R"),
            Person(last_name="Reeves", first_name="G", initial="G"),
            Person(last_name="Brinton", first_name="L", initial="L"),
            Person(last_name="Marchbanks", first_name="P", initial="P"),
            Person(last_name="Negri", first_name="E", initial="E"),
            Person(last_name="Ness", first_name="R", initial="R"),
            Person(last_name="Peeters", first_name="P H M", initial="P"),
            Person(last_name="Vessey", first_name="M", initial="M"),
            Person(last_name="Gapstur", first_name="S M", initial="S"),
            Person(last_name="Patel", first_name="A V", initial="A"),
            Person(last_name="Dal Maso", first_name="L", initial="L"),
            Person(last_name="Talamini", first_name="R", initial="R"),
            Person(last_name="Chetrit", first_name="A", initial="A"),
            Person(last_name="Hirsh", first_name="G", initial="G"),
            Person(last_name="Lubin", first_name="F", initial="F"),
            Person(last_name="Sadetzki", first_name="S", initial="S"),
            Person(last_name="Allen", first_name="N", initial="N"),
            Person(last_name="Beral", first_name="V", initial="V"),
            Person(last_name="Bull", first_name="D", initial="D"),
            Person(last_name="Callaghan", first_name="K", initial="K"),
            Person(last_name="Crossley", first_name="B", initial="B"),
            Person(last_name="Gaitskell", first_name="", initial=""),
            Person(last_name="Goodill", first_name="", initial=""),
            Person(last_name="Green", first_name="J", initial="J"),
            Person(last_name="Hermon", first_name="C", initial="C"),
            Person(last_name="Key", first_name="T", initial="T"),
            Person(last_name="Moser", first_name="K", initial="K"),
            Person(last_name="Reeves", first_name="G", initial="G"),
            Person(last_name="Collins", first_name="R", initial="R"),
            Person(last_name="Doll", first_name="R", initial="R"),
            Person(last_name="Peto", first_name="R", initial="R"),
            Person(last_name="Gonzalez", first_name="C A", initial="C"),
            Person(last_name="Lee", first_name="N", initial="N"),
            Person(last_name="Marchbanks", first_name="P", initial="P"),
            Person(last_name="Ory", first_name="H W", initial="H"),
            Person(last_name="Peterson", first_name="H B", initial="H"),
            Person(last_name="Wingo", first_name="P A", initial="P"),
            Person(last_name="Martin", first_name="N", initial="N"),
            Person(last_name="Pardthaisong", first_name="T", initial="T"),
            Person(last_name="Silpisornkosol", first_name="S", initial="S"),
            Person(last_name="Theetranont", first_name="C", initial="C"),
            Person(last_name="Boosiri", first_name="B", initial="B"),
            Person(last_name="Jimakorn", first_name="P", initial="P"),
            Person(last_name="Virutamasen", first_name="P", initial="P"),
            Person(last_name="Wongsrichanalai", first_name="C", initial="C"),
            Person(last_name="Tjonneland", first_name="A", initial="A"),
            Person(last_name="Titus-Ernstoff", first_name="L", initial="L"),
            Person(last_name="Byers", first_name="T", initial="T"),
            Person(last_name="Rohan", first_name="T", initial="T"),
            Person(last_name="Mosgaard", first_name="B J", initial="B"),
            Person(last_name="Vessey", first_name="M", initial="M"),
            Person(last_name="Yeates", first_name="D", initial="D"),
            Person(last_name="Freudenheim", first_name="J L", initial="J"),
            Person(last_name="Chang-Claude", first_name="J", initial="J"),
            Person(last_name="Kaaks", first_name="R", initial="R"),
            Person(last_name="Anderson", first_name="K E", initial="K"),
            Person(last_name="Folsom", first_name="A", initial="A"),
            Person(last_name="Robien", first_name="K", initial="K"),
            Person(last_name="Rossing", first_name="M A", initial="M"),
            Person(last_name="Thomas", first_name="D B", initial="D"),
            Person(last_name="Weiss", first_name="N S", initial="N"),
            Person(last_name="Riboli", first_name="E", initial="E"),
            Person(last_name="Clavel-Chapelon", first_name="F", initial="F"),
            Person(last_name="Cramer", first_name="D", initial="D"),
            Person(last_name="Hankinson", first_name="S E", initial="S"),
            Person(last_name="Tworoger", first_name="S S", initial="SS"),
            Person(last_name="Franceschi", first_name="S", initial="S"),
            Person(last_name="Negri", first_name="E", initial="E"),
            Person(last_name="Magnusson", first_name="C", initial="C"),
            Person(last_name="Riman", first_name="T", initial="T"),
            Person(last_name="Weiderpass", first_name="E", initial="E"),
            Person(last_name="Wolk", first_name="A", initial="A"),
            Person(last_name="Schouten", first_name="L J", initial="L"),
            Person(last_name="van den Brandt", first_name="P A", initial="P"),
            Person(last_name="Chantarakul", first_name="N", initial="N"),
            Person(last_name="Koetsawang", first_name="S", initial="S"),
            Person(last_name="Rachawat", first_name="D", initial="D"),
            Person(last_name="Palli", first_name="D", initial="D"),
            Person(last_name="Black", first_name="A", initial="A"),
            Person(last_name="Berrington de Gonzalez", first_name="A", initial="A"),
            Person(last_name="Brinton", first_name="L A", initial="L"),
            Person(last_name="Freedman", first_name="D M", initial="D"),
            Person(last_name="Hartge", first_name="P", initial="P"),
            Person(last_name="Hsing", first_name="A W", initial="A"),
            Person(last_name="Lacey", first_name="J V", initial="J", suffix="Jr"),
            Person(last_name="Hoover", first_name="R N", initial="R"),
            Person(last_name="Schairer", first_name="C", initial="C"),
            Person(last_name="Graff-Iversen", first_name="S", initial="S"),
            Person(last_name="Selmer", first_name="R", initial="R"),
            Person(last_name="Bain", first_name="C J", initial="C"),
            Person(last_name="Green", first_name="A C", initial="A"),
            Person(last_name="Purdie", first_name="D M", initial="D"),
            Person(last_name="Siskind", first_name="V", initial="V"),
            Person(last_name="Webb", first_name="P M", initial="P"),
            Person(last_name="McCann", first_name="S E", initial="S"),
            Person(last_name="Hannaford", first_name="P", initial="P"),
            Person(last_name="Kay", first_name="C", initial="C"),
            Person(last_name="Binns", first_name="C W", initial="C"),
            Person(last_name="Lee", first_name="A H", initial="A"),
            Person(last_name="Zhang", first_name="M", initial="M"),
            Person(last_name="Ness", first_name="R B", initial="R"),
            Person(last_name="Nasca", first_name="P", initial="P"),
            Person(last_name="Coogan", first_name="P F", initial="P"),
            Person(last_name="Palmer", first_name="J R", initial="J"),
            Person(last_name="Rosenberg", first_name="L", initial="L"),
            Person(last_name="Kelsey", first_name="J", initial="J"),
            Person(last_name="Paffenbarger", first_name="R", initial="R"),
            Person(last_name="Whittemore", first_name="A", initial="A"),
            Person(last_name="Katsouyanni", first_name="K", initial="K"),
            Person(last_name="Trichopoulou", first_name="A", initial="A"),
            Person(last_name="Trichopoulos", first_name="D", initial="D"),
            Person(last_name="Tzonou", first_name="A", initial="A"),
            Person(last_name="Dabancens", first_name="A", initial="A"),
            Person(last_name="Martinez", first_name="L", initial="L"),
            Person(last_name="Molina", first_name="R", initial="R"),
            Person(last_name="Salas", first_name="O", initial="O"),
            Person(last_name="Goodman", first_name="M T", initial="M"),
            Person(last_name="Lurie", first_name="G", initial="G"),
            Person(last_name="Carney", first_name="M E", initial="M"),
            Person(last_name="Wilkens", first_name="L R", initial="L"),
            Person(last_name="Hartman", first_name="L", initial="L"),
            Person(last_name="Manjer", first_name="J", initial="J"),
            Person(last_name="Olsson", first_name="H", initial="H"),
            Person(last_name="Grisso", first_name="J A", initial="J"),
            Person(last_name="Morgan", first_name="M", initial="M"),
            Person(last_name="Wheeler", first_name="J E", initial="J"),
            Person(last_name="Peeters", first_name="P H M", initial="P"),
            Person(last_name="Casagrande", first_name="J", initial="J"),
            Person(last_name="Pike", first_name="M C", initial="M"),
            Person(last_name="Ross", first_name="R K", initial="R"),
            Person(last_name="Wu", first_name="A H", initial="A"),
            Person(last_name="Miller", first_name="A B", initial="A"),
            Person(last_name="Kumle", first_name="M", initial="M"),
            Person(last_name="Lund", first_name="E", initial="E"),
            Person(last_name="McGowan", first_name="L", initial="L"),
            Person(last_name="Shu", first_name="X O", initial="X"),
            Person(last_name="Zheng", first_name="W", initial="W"),
            Person(last_name="Farley", first_name="T M M", initial="T"),
            Person(last_name="Holck", first_name="S", initial="S"),
            Person(last_name="Meirik", first_name="O", initial="O"),
            Person(last_name="Risch", first_name="H A", initial="H"),
        ]
        for i in investigators:
            if not i.cname:
                i.investigator = True
        for received, expected in zip(record["authors"], investigators, strict=False):
            assert received == expected

    def check_pub_data(self, pub: JournalRecord):
        assert (
            pub.title
            == "Use of agricultural pesticides and prostate cancer risk in the Agricultural Health Study cohort."
        )
        assert pub.medium == "Print"
        assert pub.doi == "10.1093/aje/kwg040"
        assert pub.pmc is None
        expected = (
            Person(last_name="Alavanja", first_name="Michael C R", initial="MC"),
            Person(last_name="Samanic", first_name="Claudine", initial="C"),
            Person(last_name="Dosemeci", first_name="Mustafa", initial="M"),
            Person(last_name="Lubin", first_name="Jay", initial="J"),
            Person(last_name="Tarone", first_name="Robert", initial="R"),
            Person(last_name="Lynch", first_name="Charles F", initial="CF"),
            Person(last_name="Knott", first_name="Charles", initial="C"),
            Person(last_name="Thomas", first_name="Kent", initial="K"),
            Person(last_name="Hoppin", first_name="Jane A", initial="JA"),
            Person(last_name="Barker", first_name="Joseph", initial="J"),
            Person(last_name="Coble", first_name="Joseph", initial="J"),
            Person(last_name="Sandler", first_name="Dale P", initial="DP"),
            Person(last_name="Blair", first_name="Aaron", initial="A"),
        )
        for r, e in zip(pub.authors, expected, strict=False):
            # we didn't enter affiliations, it won't match
            self.compare_author(r, e)
        assert pub.journal == "American journal of epidemiology"
        assert pub.medlineta == "Am J Epidemiol"
        assert pub.volume == "157"
        assert pub.issue == "9"
        assert pub.pubdate == "2003 May 1"
        assert pub.medlinecountry == "United States"
        assert pub.nlmuniqueid == "7910653"
        assert pub.medlinestatus == "MEDLINE"
        assert pub.pubtypelist == ["Journal Article"]
        assert pub.mesh == [
            "Adult",
            "Age Distribution",
            "Aged",
            "Agricultural Workers' Diseases",
            "Cohort Studies",
            "Humans",
            "Incidence",
            "Iowa",
            "Male",
            "Middle Aged",
            "North Carolina",
            "Odds Ratio",
            "Pesticides",
            "Prostatic Neoplasms",
            "Surveys and Questionnaires",
        ]
        assert pub.pagination == "800-14"
        expected = [
            Abstract(
                label="",
                nlmcategory="",
                text="The authors examined the relation between 45 common agricultural pesticides and prostate "
                "cancer incidence in a prospective cohort study of 55,332 male pesticide applicators from "
                "Iowa and North Carolina with no prior history of prostate cancer. Data were collected by "
                "means of self-administered questionnaires completed at enrollment (1993-1997). Cancer incidence "
                "was determined through population-based cancer registries from enrollment through December 31, "
                "1999. A prostate cancer standardized incidence ratio was computed for the cohort. Odds ratios "
                "were computed for individual pesticides and for pesticide use patterns identified by means of "
                "factor analysis. A prostate cancer standardized incidence ratio of 1.14 (95% confidence "
                "interval: 1.05, 1.24) was observed for the Agricultural Health Study cohort. Use of chlorinated "
                "pesticides among applicators over 50 years of age and methyl bromide use were significantly "
                "associated with prostate cancer risk. Several other pesticides showed a significantly increased "
                "risk of prostate cancer among study subjects with a family history of prostate cancer but not "
                "among those with no family history. Important family history-pesticide interactions were "
                "observed.",
            )
        ]
        for r, e in zip(pub.abstract, expected, strict=False):
            assert r == e
        assert pub.grants == []
        assert pub.pubstatus == "ppublish"

    def test_pubmed_fetch(self):
        """Take an existing record and use @@pubmed-compare"""
        record = entrez.get_publication("12727674")
        self.check_pub_data(record)

    def test_grants(self):
        """Tests stripping out some white text"""
        record = entrez.get_publication("18640298")
        assert record["grants"] == [
            Grant(grantid="F32 CA130434-01", acronym="CA", agency="NCI NIH HHS"),
            Grant(grantid="T32 CA09168-30", acronym="CA", agency="NCI NIH HHS"),
        ]

    def test_generate_search_string(self):
        """biopython will not take non-ascii chars"""
        search = entrez.generate_search_string(
            authors=["\xe9"], title="\xe9", journal="\xe9", pmid="", mesh="", gr="", ir="", affl="", doi=""
        )
        assert search == 'e[au]+e[ti]+"e"[jour]'

    def test_pmc_search(self):
        """Get the PMID from PMC"""
        assert entrez.get_pmid_by_pmc("4909985") == "27291797"
        assert entrez.get_pmid_by_pmc("PMC4909985") == "27291797"

    def test_validyn(self):
        record = entrez.get_publication("20051087")
        expected = [
            Person(
                last_name="Elder", collective_name="", initial="JP", first_name="John P", suffix="", investigator=False
            ),
            Person(
                last_name="Arredondo",
                collective_name="",
                initial="EM",
                first_name="Elva M",
                suffix="",
                investigator=False,
            ),
            Person(
                last_name="Campbell", collective_name="", initial="N", first_name="Nadia", suffix="", investigator=False
            ),
            Person(
                last_name="Baquero",
                collective_name="",
                initial="B",
                first_name="Barbara",
                suffix="",
                investigator=False,
            ),
            Person(
                last_name="Duerksen", collective_name="", initial="S", first_name="Susan", suffix="", investigator=False
            ),
            Person(
                last_name="Ayala",
                collective_name="",
                initial="G",
                first_name="Guadalupe",
                suffix="",
                investigator=False,
            ),
            Person(
                last_name="Crespo", collective_name="", initial="NC", first_name="Noe C", suffix="", investigator=False
            ),
            Person(
                last_name="Slymen", collective_name="", initial="D", first_name="Donald", suffix="", investigator=False
            ),
            Person(
                last_name="McKenzie",
                collective_name="",
                initial="T",
                first_name="Thomas",
                suffix="",
                investigator=False,
            ),
        ]
        for r, e in zip(record["authors"], expected, strict=False):
            # we didn't enter affiliations, it won't match
            self.compare_author(r, e)

    def test_print_electronic_pubmodel(self):
        """Both dates should be stored and the citation reflect it"""
        record = entrez.get_publication(pmid="10854512")
        assert (
            citations.journal_citation(html=True, publication=record)
            == '<span class="citation">Soon MS, Lin OS. Inflammatory fibroid polyp of the duodenum. '
            "<i>Surg Endosc</i> 2000 Jan;14(1):86. Epub 1999 Nov 25.</span>"
        )

    def test_electronic_print_pubmodel(self):
        """Both dates should be stored but use electronic date for citation"""
        record = entrez.get_publication(pmid="14729922")
        assert (
            citations.journal_citation(html=True, publication=record)
            == '<span class="citation">Edgar RC. Local homology recognition and distance measures in linear time '
            "using compressed amino acid alphabets. <i>Nucleic Acids Res</i> 2004 Jan 16;32(1):380-5. "
            "Print 2004.</span>"
        )

    def test_electronic_ecollection_pubmodel(self):
        """Both dates should be stored but use electronic date for citation"""
        record = entrez.get_publication(pmid="23372575")
        assert (
            citations.journal_citation(html=True, publication=record)
            == '<span class="citation">Wangari-Talbot J, Chen S. Genetics of melanoma. <i>Front Genet</i> 2013 '
            "Jan 25;3:330. doi: 10.3389/fgene.2012.00330. eCollection 2012.</span>"
        )

    def test_book_parse(self):
        """Be able to parse a book"""
        result = entrez.get_publication(pmid="22593940")

        assert result.volume == ""
        assert result.volumetitle == ""
        assert result.edition == "2nd"
        assert result.series == ""
        assert result.isbn == "9781439807132"
        assert result.elocation == []
        assert result.medium == ""
        assert result.reportnum == ""
        assert result.pubdate == "2011"
        assert result.pmid == "22593940"
        assert result.sections == [
            Section(title="INTRODUCTION", section_type="section", label="17.1"),
            Section(title="ALLSPICE", label="17.2", section_type="section"),
            Section(title="BASIL", section_type="section", label="17.3"),
            Section(title="CARAWAY", section_type="section", label="17.4"),
            Section(title="CARDAMOM", section_type="section", label="17.5"),
            Section(title="CINNAMON", section_type="section", label="17.6"),
            Section(title="CLOVE", section_type="section", label="17.7"),
            Section(title="CORIANDER", section_type="section", label="17.8"),
            Section(title="CUMIN", section_type="section", label="17.9"),
            Section(title="DILL", section_type="section", label="17.10"),
            Section(title="GARLIC", section_type="section", label="17.11"),
            Section(title="GINGER", section_type="section", label="17.12"),
            Section(title="ROSEMARY", section_type="section", label="17.13"),
            Section(title="SAFFRON", section_type="section", label="17.14"),
            Section(title="THYME", section_type="section", label="17.15"),
            Section(title="CONCLUSION", section_type="section", label="17.16"),
            Section(title="REFERENCES", section_type="", label=""),
        ]

        assert result.publisher == "CRC Press/Taylor & Francis"
        assert result.pubplace == "Boca Raton (FL)"
        assert result.title == "Herbs and Spices in Cancer Prevention and Treatment"
        assert result.booktitle == "Herbal Medicine: Biomolecular and Clinical Aspects"
        assert result.abstract == [
            Abstract(
                text="More than 180 spice-derived compounds have been identified and explored for their "
                "health benefits (Aggarwal et al. 2008). It is beyond the scope of this chapter to "
                "deal with all herbs and spices that may influence the risk of cancer and tumor "
                "behavior. Therefore, a decision was made to review those with some of the more "
                "impressive biological responses reported in the literature, and a conscious effort "
                "was made to provide information about the amount of spices needed to bring about a "
                "response and thus their physiological relevance. When possible, recent reviews are "
                "included to provide readers with additional insights into the biological response(s) "
                "to specific spices and to prevent duplication of the scientific literature. Because "
                "there is a separate chapter devoted to curcumin (a bioactive component in turmeric) "
                "in this book and there are also several excellent reviews published about curcumin "
                "(Patel and Majumdar 2009; Aggarwal 2010; Bar-Sela, Epelbaum, and Schaffer 2010; "
                "Epstein, Sanderson, and Macdonald 2010), turmeric is not discussed in this chapter.",
                label="",
                nlmcategory="",
            )
        ]
        assert result.language == "eng"
        authors = [
            Person(last_name="Kaefer", initial="CM", first_name="Christine M."),
            Person(last_name="Milner", initial="JA", first_name="John A."),
        ]
        editors = [
            Person(last_name="Benzie", initial="IFF", first_name="Iris F. F."),
            Person(last_name="Wachtel-Galor", initial="S", first_name="Sissi"),
        ]
        for e, r in zip(authors, result.authors, strict=False):
            assert e == r
        for e, r in zip(editors, result.editors, strict=False):
            assert e == r

    def test_find_and_fetch(self):
        record = entrez.find_publications(pmid="12727674")
        assert len(record["IdList"]) == 1
        record = entrez.get_searched_publications(record["WebEnv"], record["QueryKey"])
        self.check_pub_data(record[0])

    def test_orcid_search(self):
        record = entrez.find_publications(author_ids=["0000-0002-8953-3940"])
        assert int(record["Count"]) > 0

    def test_pubmed_orcid_author(self):
        record = entrez.get_publication(pmid="32570285")
        assert record.authors[0].orcid == "0000-0002-1771-9287"
        assert record.authors[0].asdict()["orcid"] == "0000-0002-1771-9287"

    def test_full_identifiers(self):
        record = entrez.get_publication(pmid="32570285")
        assert record.authors[0].identifiers == {"ORCID": "0000-0002-1771-9287"}

    def test_get_orcid(self):
        record = orcid.get_author(orcid="0000-0002-1771-9287")
        assert record["given_name"] == "Rachel"
        assert record["family_name"] == "Altshuler"
