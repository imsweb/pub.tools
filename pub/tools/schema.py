import dataclasses
from html import unescape
from logging import getLogger

logger = getLogger('pub.tools')


@dataclasses.dataclass
class Person:
    last_name: str
    first_name: str
    initial: str
    collective_name: str = ''
    suffix: str = ''
    investigator: bool = False
    affiliations: list[str] = dataclasses.field(default_factory=list)

    def asdict(self):
        base = dataclasses.asdict(self)
        base.update({
            'lname': self.lname,
            'fname': self.fname,
            'cname': self.cname,
            'iname': self.iname,
        })
        return base

    @property
    def lname(self):
        """ backwards compatibility """
        return self.last_name

    @property
    def fname(self):
        """ backwards compatibility """
        return self.first_name

    @property
    def iname(self):
        """ backwards compatibility """
        return self.initial

    @property
    def cname(self):
        """ backwards compatibility """
        return self.collective_name


@dataclasses.dataclass
class Abstract:
    text: str
    nlmcategory: str
    label: str


@dataclasses.dataclass
class Grant:
    grantid: str
    acronym: str
    agency: str


@dataclasses.dataclass
class Section:
    title: str
    section_type: str
    label: str

    @property
    def type(self):
        return self.section_type


@dataclasses.dataclass(kw_only=True)
class EntrezRecord:
    # type: str
    title: str
    authors: list[Person]
    pubdate: str
    pagination: str = ''
    volume: str = ''
    pmid: str = ''
    medium: str = ''
    abstract: list[Abstract] = dataclasses.field(default_factory=list)
    article_ids: dict[str, str] = dataclasses.field(default_factory=dict)

    def asdict(self):
        base = dataclasses.asdict(self)
        base.update(**{name: val for name, val in self.article_ids.items()})
        return base

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(item)

    def process(self, escape=False):
        """
        This should be called after instantiation. This removes the Biopython StringElement class and
        escapes
        """

        def munge(val, escape=False):
            if isinstance(val, list):
                return [munge(v, escape) for v in val]
            elif isinstance(val, dict):
                return {k: munge(v, escape) for k, v in val.items()}
            elif dataclasses.is_dataclass(val):
                for f in dataclasses.fields(val):
                    setattr(val, f.name, munge(getattr(val, f.name), escape))
                return val
            elif isinstance(val, str):
                if escape:
                    return unescape(str(val))  # this removes the BioPython StringElement class
                else:
                    return str(val)
            else:
                logger.info(f'Unknown type from Biopython: {type(val)}')
                return val

        for field in dataclasses.fields(self):
            field = field.name
            if escape and field not in ['title', 'abstract']:
                setattr(self, field, munge(getattr(self, field), escape=escape))
            else:
                # we expect these to be HTML, don't escape HTML entities
                setattr(self, field, munge(getattr(self, field)))


@dataclasses.dataclass
class JournalRecord(EntrezRecord):
    journal: str
    issue: str
    pubmodel: str
    pubstatus: str = ''
    grants: list[Grant] = dataclasses.field(default_factory=list)
    mesh: list[str] = dataclasses.field(default_factory=list)
    pubtypelist: list[str] = dataclasses.field(default_factory=list)
    edate: str = ''
    journal_abbreviation: str = ''
    nlmuniqueid: str = ''
    medlinecountry: str = ''
    medlinestatus: str = ''

    # very specific publication dates, you probably don't need this
    pmpubdates: dict[str, str] = dataclasses.field(default_factory=dict)

    pub_type = 'journal'

    def asdict(self):
        base = dataclasses.asdict(self)
        base['medlineta'] = self.medlineta
        base['doi'] = self.doi
        base['pmc'] = self.pmc
        base.update(**{name: val for name, val in self.pmpubdates})
        return base

    @property
    def doi(self):
        return self.article_ids.get('doi', None)

    @property
    def pmc(self):
        return self.article_ids.get('pmc', None)

    @property
    def medlineta(self):
        return self.journal_abbreviation

    # backwards compatibility
    @property
    def pmpubdate_received(self):
        return self.pmpubdates.get('pmpubdate_received', None)

    @property
    def pmpubdate_accepted(self):
        return self.pmpubdates.get('pmpubdate_accepted', None)

    @property
    def pmpubdate_entrez(self):
        return self.pmpubdates.get('pmpubdate_entrez', None)

    @property
    def pmpubdate_pubmed(self):
        return self.pmpubdates.get('pmpubdate_pubmed', None)

    @property
    def pmpubdate_medline(self):
        return self.pmpubdates.get('pmpubdate_medline', None)

    @property
    def pmpubdate_pmcrelease(self):
        return self.pmpubdates.get('pmpubdate_pmcrelease', None)


@dataclasses.dataclass(kw_only=True)
class BookRecord(EntrezRecord):
    editors: list[Person] = dataclasses.field(default_factory=list)
    publisher: str = ''
    pubplace: str = ''
    volumetitle: str = ''
    edition: str = ''
    series: str = ''
    isbn: str = ''
    language: str = ''
    elocation: str = ''
    reportnum: str = ''
    sections: list[Section] = dataclasses.field(default_factory=list)

    pub_type = 'book'


@dataclasses.dataclass
class ChapterRecord(BookRecord):
    booktitle: str = ''

    pub_type = 'chapter'


@dataclasses.dataclass
class ConferenceRecord(EntrezRecord):
    place: str = ''
    conferencename: str = ''
    conferencedate: str = ''
    publisher: str = ''
    pubplace: str = ''


@dataclasses.dataclass
class MonographRecord(EntrezRecord):
    reportnum: str = ''
    publisher: str = ''
    pubplace: str = ''
    weburl: str = ''
    series: str = ''
    serieseditors: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ReportRecord(EntrezRecord):
    editors: list[Person] = dataclasses.field(default_factory=list)
    reportnum: str = ''
    publisher: str = ''
    pubplace: str = ''
    series: str = ''
    weburl: str = ''
