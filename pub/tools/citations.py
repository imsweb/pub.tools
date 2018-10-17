import warnings
from six import StringIO
from html import escape

from .cooking import su

punc_endings = ('.', '?', '!')


def safe_escape(text):
    text = escape(text)
    text = text.replace('&lt;i&gt;', '<i>')
    text = text.replace('&lt;/i&gt;', '</i>')
    return text


def cooked_citation(func):
    def wrapper(**kwargs):
        text = func(**kwargs)
        if kwargs.get('use_abstract'):
            return text.replace('\n', '').strip()
        else:
            return safe_escape(text.replace('\n', '').strip())

    return wrapper


def punctuate(text, punctuation, space=u''):
    text = su(text)
    if not text:
        return text
    if punctuation in punc_endings and text[-1] in punc_endings:
        return text + space
    elif punctuation not in punc_endings and text[-1] == punctuation:
        return text + space
    elif text[-1] == u' ':
        return punctuate(text.strip(), punctuation, space)
    else:
        return text + punctuation + space


def period(text):
    return punctuate(text, u'.', u' ')


def comma(text):
    return punctuate(text, u',', u' ')


def colon(text):
    return punctuate(text, u':', u' ')


def colon_no_space(text):
    return punctuate(text, u':', u'')


def semi_colon(text):
    return punctuate(text, u';', u' ')


def semi_colon_no_space(text):
    return punctuate(text, u';', u'')


def cookauthor(author):
    if isinstance(author, dict):
        suffix = author.get('suffix') and ' ' + author['suffix'] or ''
        initial = author.get('iname') or author.get('fname') and author['fname'][0].upper() or ''
        if initial:
            initial = ' ' + initial
        return (author.get('cname', '') or author.get('lname') or '') + initial + suffix
    return author


@cooked_citation
def book_citation(authors=(), editors=(), title='', pubdate='', pagination='',
                  edition='', series='', pubplace='', publisher='', **kwargs):
    out = StringIO()
    if editors and not authors:
        out.write(period(u'{}, editor{}'.format(
            ', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or ''))  + '\n')
    if authors:
        out.write(period(u', '.join([su(cookauthor(a).replace(',', ' ')) for a in authors])) + '\n')
    if title:
        out.write(period(title) + '\n')
    if edition:
        out.write(period(edition) + '\n')
    if editors and authors:
        out.write(period(u'{}, editor{}'.format(
            ', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or ''))  + '\n')
    if pubplace:
        if publisher:
            out.write(colon(pubplace) + '\n')
        else:
            out.write(period(pubplace) + '\n')
    if publisher:
        if pubdate:
            out.write(semi_colon(publisher) + '\n')
        else:
            out.write(period(publisher) + '\n')
    if pubdate:
        out.write(period(pubdate) + '\n')
    if pagination:
        out.write(u'p. {0}'.format(period(pagination)) + '\n')
    if series:
        out.write(u'({})'.format(series) + '\n')
    return out.getvalue()


@cooked_citation
def chapter_citation(authors=(), editors=(), title='', pubdate='', pagination='',
                     edition='', series='', pubplace='', booktitle='', publisher='', **kwargs):
    out = StringIO()
    if editors and not authors:
        out.write(period(u'{}, editor{}'.format(
            ', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or '')) + '\n')
    if authors:
        out.write(period(u', '.join([su(cookauthor(a).replace(',', ' ')) for a in authors])) + '\n')
    if title:
        out.write(period(title) + '\n')
    if edition or editors or booktitle:
        out.write(u'In: ' + '\n')
    if editors and authors:
        out.write(period(u'{}, editor{}'.format(
            ', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or '')) + '\n')
    if booktitle:
        out.write(period(booktitle) + '\n')
    if edition:
        out.write(period(edition) + '\n')
    if pubplace:
        if publisher:
            out.write(colon(pubplace) + '\n')
        else:
            out.write(period(pubplace) + '\n')
    if publisher:
        if pubdate:
            out.write(semi_colon(publisher) + '\n')
        else:
            out.write(period(publisher) + '\n')
    if pubdate:
        out.write(period(pubdate) + '\n')
    if pagination:
        out.write(u'p. {}'.format(period(pagination)) + '\n')
    if series:
        out.write(u'({})'.format(series) + '\n')
    return out.getvalue()


@cooked_citation
def conference_citation(authors=(), editors=(), title='', pubdate='', pagination='', pubplace='', place='',
                        conferencename='', conferencedate='', publisher='', italicize=None, **kwargs):
    if italicize is None:
        warnings.warn(
            "Use the 'italicize' boolean parameter to include <i> tags. The current default is True but "
            "will be False in a future release",
            DeprecationWarning)
        italicize = True
    out = StringIO()
    if editors and not authors:
        out.write(period(u'{}, editor{}'.format(
            ', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or '')) + '\n')
    if authors:
        out.write(period(u', '.join([su(cookauthor(a).replace(',', ' ')) for a in authors])) + '\n')
    if title:
        out.write(period(title) + '\n')
    if editors and authors:
        out.write(period(u'{}, editor{}'.format(
            ', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or '')) + '\n')
    if conferencename and italicize:
        out.write(semi_colon(u'<i>Proceedings of {}</i>'.format(conferencename)) + '\n')
    elif conferencename:
        out.write(semi_colon(conferencename) + '\n')
    if conferencedate:
        if place or pubdate or publisher:
            out.write(semi_colon(conferencedate) + '\n')
        else:
            out.write(period(conferencedate) + '\n')
    if place:
        out.write(period(place) + '\n')
    if pubplace:
        if publisher or pubdate:
            out.write(colon(pubplace) + '\n')
        else:
            out.write(period(pubplace) + '\n')
    if publisher:
        if pubdate:
            out.write(semi_colon(publisher) + '\n')
        else:
            out.write(period(publisher) + '\n')
    if pubdate:
        out.write(period(pubdate) + '\n')
    if pagination:
        out.write(u'p. {}'.format(period(pagination)) + '\n')
    return out.getvalue()


@cooked_citation
def journal_citation(authors=(), title='', journal='', pubdate='', volume='', issue='', pagination='', abstract=None,
                     pubmodel='Print', edate='', doi='', pmid='', use_abstract=False, italicize=None, **kwargs):
    if italicize is None:
        warnings.warn(
            "Use the 'italicize' boolean parameter to include <i> tags. The current default is True but "
            "will be False in a future release",
            DeprecationWarning, stacklevel=2)
        italicize = True
    if not abstract:
        abstract = {}
    out = StringIO()
    if not use_abstract:
        if authors:
            out.write(period(u', '.join([su(cookauthor(a).replace(',', ' ')) for a in authors if a])) + '\n')
        if title:
            out.write(period(title) + '\n')
        if journal and italicize:
            out.write(u'<i>{}</i> '.format(su(journal).strip()) + '\n')
        elif journal:
            out.write(period(su(journal).strip()) + '\n')

        if pubmodel in ('Print', 'Electronic', 'Print-Electronic'):  # use the publication date
            date = pubdate
        elif pubmodel in ('Electronic-Print', 'Electronic-eCollection'):  # use the electronic date
            date = edate
        else:
            date = pubdate or edate

        if date:
            if pagination and not (volume or issue):
                out.write(colon(date) + '\n')
            elif volume or issue:
                out.write(semi_colon_no_space(date) + '\n')
            else:
                out.write(period(date) + '\n')
        if volume:
            if pagination and not issue:
                out.write(colon_no_space(volume) + '\n')
            elif pagination:
                out.write(volume + '\n')
            else:
                out.write(period(volume) + '\n')
        if issue:
            if pagination:
                out.write(colon_no_space(u'({})'.format(issue)) + '\n')
            else:
                out.write(period(u'({})'.format(issue)) + '\n')
        if pagination:
            out.write(period(pagination) + '\n')
        if pubmodel in ('Print-Electronic',):
            if edate:
                out.write('Epub ' + period(edate) + '\n')
        if pubmodel in ('Electronic-Print',):
            if pubdate:
                out.write('Print ' + period(pubdate) + '\n')
        if pubmodel in ('Electronic-eCollection',):
            if pubdate:
                if doi:
                    out.write('doi: {}. eCollection {}'.format(doi, period(pubdate)) + '\n')
                else:
                    out.write('eCollection {}'.format(period(pubdate)) + '\n')

    else:
        out.write(u'<b>Author: </b>{}<br/>'.format(u', '.join([su(cookauthor(a)).replace(u',', u' ') for a in authors])) + '\n')
        out.write(u'<b>Title: </b>{}<br/>'.format(title) + '\n')
        out.write(u'<b>Journal: </b>{}'.format(journal) + '\n')
        if journal and issue and volume and pagination:
            out.write(u'. {volume}({issue}):{pagination}'.format(volume=volume, issue=issue, pagination=pagination) + '\n')
        out.write(u'<br/>' + '\n')
        out.write(u'<b>Pubmed link: </b><a href="http://www.ncbi.nlm.nih.gov/pubmed/{0}">' \
                      u'http://www.ncbi.nlm.nih.gov/pubmed/{0}</a><br/>'.format(pmid) + '\n')
        if pubmodel in ('Print', 'Electronic', 'Print-Electronic'):  # use the publication date
            date = pubdate
        elif pubmodel in ('Electronic-Print', 'Electronic-eCollection'):  # use the electronic date
            date = edate
        else:
            date = pubdate or edate
        out.write(u'<b>Citation Date: </b>{}'.format(date) + '\n')
        if pubmodel in ('Print-Electronic',):
            if edate:
                out.write(u'. Epub {}<br/>'.format(period(edate)) + '\n')
        elif pubmodel in ('Electronic-Print',):
            if pubdate:
                out.write(u'. Print {}<br/>'.format(period(pubdate)) + '\n')
        elif pubmodel in ('Electronic-eCollection',):
            if pubdate:
                if doi:
                    out.write(u'doi: {}. eCollection {}<br/>'.format(doi, period(pubdate)) + '\n')
                else:
                    out.write(u'eCollection {}<br/>'.format(period(pubdate)) + '\n')
        else:
            out.write(u'<br/>' + '\n')
        abstracts = []
        for seg in abstract:
            abst = seg.get('label') or ''
            abst += abst and ': ' or ''
            abst += seg.get('text') or ''
            if abst:
                abstracts.append(abst)
        abstract = ' '.join(abstracts)
        out.write(u'<b>Abstract: </b>{}<br/>'.format(su(abstract)) + '\n')
    return out.getvalue()


@cooked_citation
def monograph_citation(authors=(), title='', pubdate='', series='', pubplace='', weburl='', reportnum='', publisher='',
                       serieseditors=(), **kwargs):
    out = StringIO()
    if serieseditors and not authors:
        out.write(period(u'{}, editor{}'.format(
            ', '.join([su(cookauthor(e).replace(',', ' ')) for e in serieseditors]),
            len(serieseditors) > 1 and 's' or '')) + '\n')
    if authors:
        out.write(semi_colon(u', '.join([su(cookauthor(a).replace(',', ' ')) for a in authors])) + '\n')
    if title:
        out.write(period(title) + '\n')
    if series:
        out.write(period(series) + '\n')
    if serieseditors and authors:
        out.write(period(u'{}, editor{}'.format(
            ', '.join([su(cookauthor(e).replace(',', ' ')) for e in serieseditors]),
            len(serieseditors) > 1 and 's' or '')) + '\n')
    if pubplace:
        if publisher:
            out.write(colon(pubplace) + '\n')
        elif pubdate:
            out.write(semi_colon(pubplace) + '\n')
        else:
            out.write(period(pubplace) + '\n')
    if publisher:
        if pubdate:
            out.write(semi_colon(publisher) + '\n')
        else:
            out.write(period(publisher) + '\n')
    if pubdate:
        out.write(period(pubdate) + '\n')
    if reportnum:
        out.write(period(reportnum) + '\n')
    if weburl:
        out.write(u'Available at {0}.'.format(weburl) + '\n')
    return out.getvalue()


@cooked_citation
def report_citation(authors=(), editors=(), title='', pubdate='', pagination='', series='', pubplace='', weburl='',
                    reportnum='', publisher='', **kwargs):
    out = StringIO()
    if editors and not authors:
        out.write(period(u'{}, editor{}'.format(
            ', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or '')) + '\n')
    if authors:
        out.write(period(u', '.join([su(cookauthor(a).replace(',', ' ')) for a in authors])) + '\n')
    if title:
        out.write(period(title) + '\n')
    if series:
        out.write(period(series) + '\n')
    if editors and authors:
        out.write(period(u'{}, editor{}'.format(
            ', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or '')) + '\n')
    if pubplace:
        if publisher:
            out.write(colon(pubplace) + '\n')
        elif pubdate:
            out.write(semi_colon(pubplace) + '\n')
        else:
            out.write(period(pubplace) + '\n')
    if publisher:
        if pubdate:
            out.write(semi_colon(publisher) + '\n')
        else:
            out.write(period(publisher) + '\n')
    if pubdate:
        out.write(period(pubdate) + '\n')
    if reportnum:
        out.write(period(reportnum) + '\n')
    if pagination:
        out.write(period(u'p. {0}'.format(pagination)) + '\n')
    if weburl:
        out.write(u'Available at {0}.'.format(weburl) + '\n')
    return out.getvalue()
