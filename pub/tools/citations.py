from io import StringIO
from bs4 import BeautifulSoup
from lxml import etree as et
from collections.abc import Callable
import dataclasses
from .schema import Person
from .schema import JournalRecord
from .schema import BookRecord
from .schema import ChapterRecord
from .schema import Abstract
from .schema import EntrezRecord

WRAPPER_TAG = 'cite'
PUNC_ENDINGS = ('.', '?', '!')


def cooked_citation(func: Callable):
    def wrapper(**kwargs):
        text = func(**kwargs)
        try:
            et.XML(text)
        except et.XMLSyntaxError:
            # try to escape ampersands, prevent double escape
            text = text.replace("&amp;", "$$_pubtools_amp;")
            text = text.replace("&lt;", "$$_pubtools_lt;")
            text = text.replace("&gt;", "$$_pubtools_gt;")
            text = text.replace("&quot;", "$$_pubtools_quot;")
            text = text.replace("&", "&amp;")
            text = text.replace("$$_pubtools_amp;", "&amp;")
            text = text.replace("$$_pubtools_lt;", "&lt;")
            text = text.replace("$$_pubtools_gt;", "&gt;")
            text = text.replace("$$_pubtools_quot;", "&quot;")
        if kwargs.get('use_abstract'):
            return text.replace('\n', '').strip()
        else:
            return text.strip()

    return wrapper


def punctuate(text, punctuation, space=''):
    soup = BeautifulSoup(text, 'html.parser')
    element = soup.find('a')
    if not text:
        return text
    if punctuation in PUNC_ENDINGS and text[-1] in PUNC_ENDINGS or (element and element.get_text()[-1] in PUNC_ENDINGS):
        return text + space
    elif punctuation not in PUNC_ENDINGS and text[-1] == punctuation:
        return text + space
    elif text[-1] == ' ':
        return punctuate(text.strip(), punctuation, space)
    else:
        return text + punctuation + space


def period(text):
    return punctuate(text, '.', ' ')


def comma(text):
    return punctuate(text, ',', ' ')


def colon(text):
    return punctuate(text, ':', ' ')


def colon_no_space(text):
    return punctuate(text, ':', '')


def semi_colon(text):
    return punctuate(text, ';', ' ')


def semi_colon_no_space(text):
    return punctuate(text, ';', '')


def cookauthor(author, suffix=True):
    """ Deprecated"""
    return citation_author(author, use_suffix=suffix)


def citation_author(author: Person | dict, use_suffix: bool = True):
    if not isinstance(author, Person):
        author = {
            'last_name': author.get('lname') or author.get('last_name'),
            'first_name': author.get('fname') or author.get('first_name'),
            'collective_name': author.get('cname') or author.get('collective_name'),
            'initial': author.get('iname') or author.get('initial'),
            'suffix': author.get('suffix') or author.get('suffix'),
        }
        return citation_author(Person(**author))
    initial = author.iname if author.iname else author.fname[0].upper()
    lname = author.cname or author.lname
    parts = [lname, initial]
    if use_suffix and author.suffix:
        parts.append(author.suffix)
    return ' '.join([p.rstrip() for p in parts if p])


@cooked_citation
def book_citation(authors: list[Person | dict] = (), editors: list[Person | dict] = (), title: str = '',
                  pubdate: str = '',
                  pagination: str = '', edition: str = '', series: str = '', pubplace: str = '', publisher: str = '',
                  html: bool = False, publication: BookRecord = None, **kwargs):
    """ book citation

        You can pass each field separately, or pass an EntrezRecord object
    """
    if publication:
        return book_citation(**publication.asdict(), html=html)
    out = StringIO()
    if html:
        out.write(f'<{WRAPPER_TAG}>')
    if editors and not authors:
        out.write(period(
            f"{', '.join([citation_author(e) for e in editors]).replace(',', ' ')}, editor{'s' if len(editors) > 1 else ''}"))
    if authors:
        out.write(period(', '.join([citation_author(a) for a in authors])))
    if title:
        out.write(period(title))
    if edition:
        out.write(period(edition))
    if editors and authors:
        out.write(period(
            f"{', '.join([citation_author(e) for e in editors]).replace(',', ' ')}, editor{'s' if len(editors) > 1 else ''}"))
    if pubplace:
        if publisher:
            out.write(colon(pubplace))
        else:
            out.write(period(pubplace))
    if publisher:
        if pubdate:
            out.write(semi_colon(publisher))
        else:
            out.write(period(publisher))
    if pubdate:
        out.write(period(pubdate))
    if pagination:
        out.write('p. {0}'.format(period(pagination)))
    if series:
        out.write('({})'.format(series))
    out = out.getvalue().strip()
    if html:
        out += f'</{WRAPPER_TAG}>'
    return out


@cooked_citation
def chapter_citation(authors: list[Person | dict] = (), editors: list[Person | dict] = (), title: str = '',
                     pubdate: str = '',
                     pagination: str = '', edition: str = '', series: str = '', pubplace: str = '', publisher: str = '',
                     booktitle: str = '', html: bool = False, publication: ChapterRecord = None, **kwargs):
    """ book chapter citation


        You can pass each field separately, or pass an EntrezRecord object
    """
    if publication:
        return chapter_citation(**publication.asdict(), html=html)
    out = StringIO()
    if html:
        out.write(f'<{WRAPPER_TAG}>')
    if editors and not authors:
        out.write(period('{}, editor{}'.format(
            ', '.join([citation_author(e).replace(',', ' ') for e in editors]), len(editors) > 1 and 's' or '')))
    if authors:
        out.write(period(', '.join([citation_author(a).replace(',', ' ') for a in authors])))
    if title:
        out.write(period(title))
    if edition or editors or booktitle:
        out.write('In: ')
    if editors and authors:
        out.write(period('{}, editor{}'.format(
            ', '.join([citation_author(e).replace(',', ' ') for e in editors]), len(editors) > 1 and 's' or '')))
    if booktitle:
        out.write(period(booktitle))
    if edition:
        out.write(period(edition))
    if pubplace:
        if publisher:
            out.write(colon(pubplace))
        else:
            out.write(period(pubplace))
    if publisher:
        if pubdate:
            out.write(semi_colon(publisher))
        else:
            out.write(period(publisher))
    if pubdate:
        out.write(period(pubdate))
    if pagination:
        out.write('p. {}'.format(period(pagination)))
    if series:
        out.write('({})'.format(series))
    out = out.getvalue().strip()
    if html:
        out += f'</{WRAPPER_TAG}>'
    return out


@cooked_citation
def conference_citation(authors: list[Person | dict] = (), editors: list[Person | dict] = (), title: str = '',
                        pubdate: str = '', pagination: str = '', pubplace: str = '', place: str = '',
                        conferencename: str = '', conferencedate: str = '', publisher: str = '', html: bool = False,
                        publication: EntrezRecord = None, **kwargs):
    """ conference citation

        You can pass each field separately, or pass an EntrezRecord object
    """
    if publication:
        return conference_citation(**publication.asdict(), html=html)
    out = StringIO()
    if html:
        out.write(f'<{WRAPPER_TAG}>')
    if editors and not authors:
        out.write(period('{}, editor{}'.format(
            ', '.join([citation_author(e).replace(',', ' ') for e in editors]), len(editors) > 1 and 's' or '')))
    if authors:
        out.write(period(', '.join([citation_author(a).replace(',', ' ') for a in authors])))
    if title:
        out.write(period(title))
    if editors and authors:
        out.write(period('{}, editor{}'.format(
            ', '.join([citation_author(e).replace(',', ' ') for e in editors]), len(editors) > 1 and 's' or '')))
    if conferencename and html:
        out.write(semi_colon('<i>Proceedings of {}</i>'.format(conferencename)))
    elif conferencename:
        out.write(semi_colon('Proceedings of {}'.format(conferencename)))
    if conferencedate:
        if place or pubdate or publisher:
            out.write(semi_colon(conferencedate))
        else:
            out.write(period(conferencedate))
    if place:
        out.write(period(place))
    if pubplace:
        if publisher or pubdate:
            out.write(colon(pubplace))
        else:
            out.write(period(pubplace))
    if publisher:
        if pubdate:
            out.write(semi_colon(publisher))
        else:
            out.write(period(publisher))
    if pubdate:
        out.write(period(pubdate))
    if pagination:
        out.write('p. {}'.format(period(pagination)))
    out = out.getvalue().strip()
    if html:
        out += f'</{WRAPPER_TAG}>'
    return out


@cooked_citation
def journal_citation(authors: list[Person | dict] = (), title: str = '', journal: str = '', pubdate: str = '',
                     volume: str = '', issue: str = '', pagination: str = '',
                     abstract: list[Abstract] = None, pubmodel: str = 'Print', edate: str = '', doi: str = '',
                     pmid: str = '', journal_abbreviation: str = '', use_abstract: bool = False,
                     html: bool = False, link: bool = False, publication: JournalRecord = None, **kwargs):
    """ journal citation

    """
    if publication:
        return journal_citation(**publication.asdict(), html=html, use_abstract=use_abstract, link=link)
    if journal_abbreviation:
        journal = journal_abbreviation
    if not abstract:
        abstract = {}
    out = StringIO()
    if html:
        out.write(f'<{WRAPPER_TAG}>')
    if authors:
        out.write(period(', '.join([citation_author(a).replace(',', ' ') for a in authors if a])))
    if title:
        if link and pmid:
            out.write(
                period(f'<a class="citation-pubmed-link" href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/">{title}</a>'))
        else:
            out.write(period(title))
    if journal and html:
        out.write('<i>{}</i> '.format(journal.strip()))
    elif journal:
        out.write(period(journal.strip()))

    if pubmodel in ('Print', 'Electronic', 'Print-Electronic'):  # use the publication date
        date = pubdate
    elif pubmodel in ('Electronic-Print', 'Electronic-eCollection'):  # use the electronic date
        date = edate
    else:
        date = pubdate or edate

    if date:
        if pagination and not (volume or issue):
            out.write(colon(date))
        elif volume or issue:
            out.write(semi_colon_no_space(date))
        else:
            out.write(period(date))
    if volume:
        if pagination and not issue:
            out.write(colon_no_space(volume))
        elif pagination:
            out.write(volume)
        else:
            out.write(period(volume))
    if issue:
        if pagination:
            out.write(colon_no_space('({})'.format(issue)))
        else:
            out.write(period('({})'.format(issue)))
    if pagination:
        out.write(period(pagination))
    if pubmodel in ('Print-Electronic',):
        if edate:
            out.write('Epub ' + period(edate))
    if pubmodel in ('Electronic-Print',):
        if pubdate:
            out.write('Print ' + period(pubdate))
    if pubmodel in ('Electronic-eCollection',):
        if pubdate:
            if doi:
                out.write('doi: {}. eCollection {}'.format(doi, period(pubdate)))
            else:
                out.write('eCollection {}'.format(period(pubdate)))

    if use_abstract:
        out.write('<br/>')
        abstracts = []
        for seg in abstract:
            abst = seg.get('label') or ''
            abst += abst and ': ' or ''
            abst += seg.get('text') or ''
            if abst:
                abstracts.append('<p>{}</p>'.format(abst))
        abstract = ' '.join(abstracts)
        if abstract:
            out.write(
                f'<div class="citationAbstract"><p class="abstractHeader">'
                f'<strong>Abstract</strong></p>{abstract}</div>'
            )
    out = out.getvalue().strip()
    if html:
        out += f'</{WRAPPER_TAG}>'
    return out


@cooked_citation
def monograph_citation(authors: list[Person | dict] = (), title: str = '', pubdate: str = '', series: str = '',
                       pubplace: str = '', weburl: str = '', reportnum: str = '', publisher: str = '',
                       serieseditors: list[str] = (), html: bool = False, publication: EntrezRecord = None, **kwargs):
    """ book chapter citation

    """
    if publication:
        return book_citation(**publication.asdict(), html=html)
    out = StringIO()
    if html:
        out.write(f'<{WRAPPER_TAG}>')
    if serieseditors and not authors:
        out.write(period(
            f"{', '.join([e.replace(',', ' ') for e in serieseditors])}, editor{'s' if len(serieseditors) > 1 else ''}"))
    if authors:
        out.write(semi_colon(', '.join([citation_author(a).replace(',', ' ') for a in authors])))
    if title:
        out.write(period(title))
    if series:
        out.write(period(series))
    if serieseditors and authors:
        out.write(period('{}, editor{}'.format(
            ', '.join([e.replace(',', ' ') for e in serieseditors]),
            len(serieseditors) > 1 and 's' or '')))
    if pubplace:
        if publisher:
            out.write(colon(pubplace))
        elif pubdate:
            out.write(semi_colon(pubplace))
        else:
            out.write(period(pubplace))
    if publisher:
        if pubdate:
            out.write(semi_colon(publisher))
        else:
            out.write(period(publisher))
    if pubdate:
        out.write(period(pubdate))
    if reportnum:
        out.write(period(reportnum))
    if weburl:
        out.write('Available at {0}.'.format(weburl))
    out = out.getvalue().strip()
    if html:
        out += f'</{WRAPPER_TAG}>'
    return out


@cooked_citation
def report_citation(authors: list[Person | dict] = (), editors: list[Person | dict] = (), title: str = '',
                    pubdate: str = '', pagination: str = '', series: str = '', pubplace: str = '', weburl: str = '',
                    reportnum: str = '', publisher: str = '', html: bool = False, publication: EntrezRecord = None,
                    **kwargs):
    """ book chapter citation

    """
    if publication:
        return book_citation(**publication.asdict(), html=html)
    out = StringIO()
    if html:
        out.write(f'<{WRAPPER_TAG}>')
    if editors and not authors:
        out.write(period('{}, editor{}'.format(
            ', '.join([citation_author(e).replace(',', ' ') for e in editors]), len(editors) > 1 and 's' or '')))
    if authors:
        out.write(period(', '.join([citation_author(a).replace(',', ' ') for a in authors])))
    if title:
        out.write(period(title))
    if series:
        out.write(period(series))
    if editors and authors:
        out.write(period('{}, editor{}'.format(
            ', '.join([citation_author(e).replace(',', ' ') for e in editors]), len(editors) > 1 and 's' or '')))
    if pubplace:
        if publisher:
            out.write(colon(pubplace))
        elif pubdate:
            out.write(semi_colon(pubplace))
        else:
            out.write(period(pubplace))
    if publisher:
        if pubdate:
            out.write(semi_colon(publisher))
        else:
            out.write(period(publisher))
    if pubdate:
        out.write(period(pubdate))
    if reportnum:
        out.write(period(reportnum))
    if pagination:
        out.write(period(f'p. {pagination}'))
    if weburl:
        out.write(f'Available at {weburl}.')
    out = out.getvalue().strip()
    if html:
        out += f'</{WRAPPER_TAG}>'
    return out


@cooked_citation
def citation(publication: JournalRecord | BookRecord | ChapterRecord, html: bool = False):
    """ Undefined publication type. Only usable with pub types that can be retrieved from Pubmed.
        Example usage:
        >>> from pub.tools import entrez
        >>> from pub.tools import citations
        >>> pub = entrez.get_publication(pmid=12345678)
        >>> citations.citation(pub)

    """
    pub_types = {
        'journal': journal_citation,
        'book': book_citation,
        'chapter': chapter_citation
    }
    return pub_types[publication.pub_type](publication=publication, html=html)
