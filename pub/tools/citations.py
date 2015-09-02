from .cooking import su
from StringIO import StringIO
from cgi import escape

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
def book_citation(authors=[], editors=[], title='', journal='', pubdate='', volume='', issue='', pagination='', edition='', series='', pubplace='', booktitle='', chapternum='', weburl='', place='', conferencename='', conferencedate='', reportnum='', publisher='', abstract='', serieseditors=[], pubmodel='Print', edate='', doi='', pmid='', use_abstract=False, **kwargs):
    out = StringIO()
    if editors and not authors:
        print >> out, period(u'%s, editor%s' % (', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or ''))
    if authors:
        print >> out, period(u', '.join([su(cookauthor(a).replace(',', ' ')) for a in authors]))
    if title:
        print >> out, period(title)
    if edition:
        print >> out, period(edition)
    if editors and authors:
        print >> out, period(u'%s, editor%s' % (', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or ''))
    if pubplace:
        if publisher:
            print >> out, colon(pubplace)
        else:
            print >> out, period(pubplace)
    if publisher:
        if pubdate:
            print >> out, semi_colon(publisher)
        else:
            print >> out, period(publisher)
    if pubdate:
        print >> out, period(pubdate)
    if pagination:
        print >> out, u'p. %s' % period(pagination)
    if series:
        print >> out, u'(%s)' % series
    return out.getvalue()

@cooked_citation
def chapter_citation(authors=[], editors=[], title='', journal='', pubdate='', volume='', issue='', pagination='', edition='', series='', pubplace='', booktitle='', chapternum='', weburl='', place='', conferencename='', conferencedate='', reportnum='', publisher='', abstract='', serieseditors=[], pubmodel='Print', edate='', doi='', pmid='', use_abstract=False, **kwargs):
    out = StringIO()
    if editors and not authors:
        print >> out, period(u'%s, editor%s' % (', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or ''))
    if authors:
        print >> out, period(u', '.join([su(cookauthor(a).replace(',', ' ')) for a in authors]))
    if title:
        print >> out, period(title)
    if edition or editors or booktitle:
        print >> out, u'In: '
    if editors and authors:
        print >> out, period(u'%s, editor%s' % (', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or ''))
    if booktitle:
        print >> out, period(booktitle)
    if edition:
        print >> out, period(edition)
    if pubplace:
        if publisher:
            print >> out, colon(pubplace)
        else:
            print >> out, period(pubplace)
    if publisher:
        if pubdate:
            print >> out, semi_colon(publisher)
        else:
            print >> out, period(publisher)
    if pubdate:
        print >> out, period(pubdate)
    if pagination:
        print >> out, u'p. %s' % period(pagination)
    if series:
        print >> out, u'(%s)' % series
    return out.getvalue()

@cooked_citation
def conference_citation(authors=[], editors=[], title='', journal='', pubdate='', volume='', issue='', pagination='', edition='', series='', pubplace='', booktitle='', chapternum='', weburl='', place='', conferencename='', conferencedate='', reportnum='', publisher='', abstract='', serieseditors=[], pubmodel='Print', edate='', doi='', pmid='', use_abstract=False, **kwargs):
    out = StringIO()
    if editors and not authors:
        print >> out, period(u'%s, editor%s' % (', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or ''))
    if authors:
        print >> out, period(u', '.join([su(cookauthor(a).replace(',', ' ')) for a in authors]))
    if title:
        print >> out, period(title)
    if editors and authors:
        print >> out, period(u'%s, editor%s' % (', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or ''))
    if conferencename:
        print >> out, semi_colon(u'<i>Proceedings of %s</i>' % conferencename)
    if conferencedate:
        if place or pubdate or publisher:
            print >> out, semi_colon(conferencedate)
        else:
            print >> out, period(conferencedate)
    if place:
        print >> out, period(place)
    if pubplace:
        if publisher or pubdate:
            print >> out, colon(pubplace)
        else:
            print >> out, period(pubplace)
    if publisher:
        if pubdate:
            print >> out, semi_colon(publisher)
        else:
            print >> out, period(publisher)
    if pubdate:
        print >> out, period(pubdate)
    if pagination:
        print >> out, u'p. %s' % period(pagination)
    return out.getvalue()

@cooked_citation
def journal_citation(authors=[], editors=[], title='', journal='', pubdate='', volume='', issue='', pagination='', edition='', series='', pubplace='', booktitle='', chapternum='', weburl='', place='', conferencename='', conferencedate='', reportnum='', publisher='', abstract='', serieseditors=[], pubmodel='Print', edate='', doi='', pmid='', use_abstract=False, **kwargs):
    out = StringIO()
    if not use_abstract:
        if authors:
            print >> out, period(u', '.join([su(cookauthor(a).replace(',', ' ')) for a in authors if a]))
        if title:
            print >> out, period(title)
        if journal:
            print >> out, u'<i>%s</i> ' % su(journal).strip()

        dat = ''
        if pubmodel in ('Print', 'Electronic', 'Print-Electronic'): # use the publication date
            dat = pubdate
        elif pubmodel in ('Electronic-Print', 'Electronic-eCollection'): # use the electronic date
            dat = edate
        else:
            dat = pubdate or edate

        if dat:
            if pagination and not (volume or issue):
                print >> out, colon(dat)
            elif volume or issue:
                print >> out, semi_colon_no_space(dat)
            else:
                print >> out, period(dat)
        if volume:
            if pagination and not issue:
                print >> out, colon_no_space(volume)
            elif pagination:
                print >> out, volume
            else:
                print >> out, period(volume)
        if issue:
            if pagination:
                print >> out, colon_no_space(u'(%s)' % issue)
            else:
                print >> out, period(u'(%s)' % issue)
        if pagination:
            print >> out, period(pagination)
        if pubmodel in ('Print-Electronic',):
            if edate:
                print >> out, 'Epub ' + period(edate)
        if pubmodel in ('Electronic-Print',):
            if pubdate:
                print >> out, 'Print ' + period(pubdate)
        if pubmodel in ('Electronic-eCollection',):
            if pubdate:
                if doi:
                    print >> out, 'doi: %s. eCollection %s' % (doi, period(pubdate))
                else:
                    print >> out, 'eCollection %s' + period(pubdate)

    else:
        print >> out, u'<b>Author: </b>%s<br/>' % u', '.join([su(cookauthor(a)).replace(u',', u' ') for a in authors])
        print >> out, u'<b>Title: </b>%s<br/>' % title
        print >> out, u'<b>Journal: </b>%s' % journal
        if journal and issue and volume and pagination:
            print >> out, u'. %s(%s):%s' % (volume, issue, pagination)
        print >> out, u'<br/>'
        print >> out, u'<b>Pubmed link: </b><a href="http://www.ncbi.nlm.nih.gov/pubmed/%s">http://www.ncbi.nlm.nih.gov/pubmed/%s</a><br/>' % (pmid, pmid)
        if pubmodel in ('Print', 'Electronic', 'Print-Electronic'): # use the publication date
            dat = pubdate
        elif pubmodel in ('Electronic-Print', 'Electronic-eCollection'): # use the electronic date
            dat = edate
        else:
            dat = pubdate or edate
        print >> out, u'<b>Citation Date: </b>%s' % dat
        if pubmodel in ('Print-Electronic',):
            if edate:
                print >> out, u'. Epub %s<br/>' % period(edate)
        elif pubmodel in ('Electronic-Print',):
            if pubdate:
                print >> out, u'. Print %s<br/>' % period(pubdate)
        elif pubmodel in ('Electronic-eCollection',):
            if pubdate:
                if doi:
                    print >> out, u'doi: %s. eCollection %s<br/>' % (doi, period(pubdate))
                else:
                    print >> out, u'eCollection %s<br/>' + period(pubdate)
        else:
            print >> out, u'<br/>'
        abstracts = []
        for seg in abstract:
            abst = seg.get('label') or ''
            abst += abst and ': ' or ''
            abst += seg.get('text') or ''
            if abst:
                abstracts.append(abst)
        abstract = ' '.join(abstracts)
        print >> out, u'<b>Abstract: </b>%s<br/>' % su(abstract)
    return out.getvalue()

@cooked_citation
def monograph_citation(authors=[], editors=[], title='', journal='', pubdate='', volume='', issue='', pagination='', edition='', series='', pubplace='', booktitle='', chapternum='', weburl='', place='', conferencename='', conferencedate='', reportnum='', publisher='', abstract='', serieseditors=[], pubmodel='Print', edate='', doi='', pmid='', use_abstract=False, **kwargs):
    out = StringIO()
    if serieseditors and not authors:
        print >> out, period(u'%s, editor%s' % (', '.join([su(cookauthor(e).replace(',', ' ')) for e in serieseditors]), len(serieseditors) > 1 and 's' or ''))
    if authors:
        print >> out, semi_colon(u', '.join([su(cookauthor(a).replace(',', ' ')) for a in authors]))
    if title:
        print >> out, period(title)
    if series:
        print >> out, period(series)
    if serieseditors and authors:
        print >> out, period(u'%s, editor%s' % (', '.join([su(cookauthor(e).replace(',', ' ')) for e in serieseditors]), len(serieseditors) > 1 and 's' or ''))
    if pubplace:
        if publisher:
            print >> out, colon(pubplace)
        elif pubdate:
            print >> out, semi_colon(pubplace)
        else:
            print >> out, period(pubplace)
    if publisher:
        if pubdate:
            print >> out, semi_colon(publisher)
        else:
            print >> out, period(publisher)
    if pubdate:
        print >> out, period(pubdate)
    if reportnum:
        print >> out, period(reportnum)
    if weburl:
        print >> out, u'Available at %s.' % weburl
    return out.getvalue()

@cooked_citation
def report_citation(authors=[], editors=[], title='', journal='', pubdate='', volume='', issue='', pagination='', edition='', series='', pubplace='', booktitle='', chapternum='', weburl='', place='', conferencename='', conferencedate='', reportnum='', publisher='', abstract='', serieseditors=[], pubmodel='Print', edate='', doi='', pmid='', use_abstract=False, **kwargs):
    out = StringIO()
    if editors and not authors:
        print >> out, period(u'%s, editor%s' % (', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or ''))
    if authors:
        print >> out, period(u', '.join([su(cookauthor(a).replace(',', ' ')) for a in authors]))
    if title:
        print >> out, period(title)
    if series:
        print >> out, period(series)
    if editors and authors:
        print >> out, period(u'%s, editor%s' % (', '.join([su(cookauthor(e).replace(',', ' ')) for e in editors]), len(editors) > 1 and 's' or ''))
    if pubplace:
        if publisher:
            print >> out, colon(pubplace)
        elif pubdate:
            print >> out, semi_colon(pubplace)
        else:
            print >> out, period(pubplace)
    if publisher:
        if pubdate:
            print >> out, semi_colon(publisher)
        else:
            print >> out, period(publisher)
    if pubdate:
        print >> out, period(pubdate)
    if reportnum:
        print >> out, period(reportnum)
    if pagination:
        print >> out, period(u'p. %s' % pagination)
    if weburl:
        print >> out, u'Available at %s.' % weburl
    return out.getvalue()
