from Bio import Entrez
from unidecode import unidecode
from . import config
from .cooking import cook_date_str, su
from httplib import IncompleteRead
import re
import time
import logging

Entrez.email = config.ENTREZ_EMAIL
Entrez.tool = config.ENTREZ_TOOL
Entrez.api_key = config.ENTREZ_API_KEY
logger = logging.getLogger('pub.tools')


class PubToolsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
IMSEntrezError = PubToolsError


def parse_entrez_record(record):
    """ convert this into our own data structure format
        Journal keys - MedlineCitation, PubmedData
        Book keys - BookDocument, PubmedBookData
    """
    if 'PubmedData' in record:
        return parse_entrez_journal_record(record)
    elif 'PubmedBookData' in record:
        return parse_entrez_book_record(record)


def parse_entrez_book_record(record):
    data = {'type': 'book'}
    document = record.pop('BookDocument')
    book = document.pop('Book')
    # publicationtype = document.pop('PublicationType') - unsure what this is
    # kwlist = document.pop('KeywordList') - unsure what this is

    authors = []
    if document.get('AuthorList', []) and document['AuthorList'][0].attributes['Type'] == 'authors':
        for author in document['AuthorList'][0]:
            for aff in author.get('AffiliationInfo', []):
                data['affiliation'] = aff['Affiliation']
            authors.append({'lname': author.get('LastName', ''),
                            'fname': author.get('ForeName', ''),
                            'iname': author.get('Initials', ''),
                            'cname': author.get('CollectiveName', ''),
                            'suffix': author.get('Suffix', ''),
                            'investigator': False})
    data['authors'] = authors

    editors = []
    if book.get('AuthorList', []) and book['AuthorList'][0].attributes['Type'] == 'editors':
        for author in book['AuthorList'][0]:
            for aff in author.get('AffiliationInfo', []):
                data['affiliation'] = aff['Affiliation']
            authors.append({'lname': author.get('LastName', ''),
                            'fname': author.get('ForeName', ''),
                            'iname': author.get('Initials', ''),
                            'cname': author.get('CollectiveName', ''),
                            'suffix': author.get('Suffix', ''),
                            'investigator': False})
    data['editors'] = editors

    data['language'] = document.get('Language', '') and document['Language'][0]

    articleids = document.pop('ArticleIdList')
    for aid in articleids:
        data[aid.attributes['IdType']] = unicode(aid)

    data['abstract'] = document.get('Abstract', {}).get('AbstractText', '')
    if isinstance(data['abstract'], list):
        data['abstract'] = data['abstract'][0]  # why does it do this?
    articletitle = su(document.get('ArticleTitle', ''))

    locationlabel = document.get('LocationLabel', '')
    if locationlabel and locationlabel[0].attributes['Type'] == 'chapter':
        data['type'] = 'chapter'
        data['title'] = articletitle
        data['booktitle'] = su(book.get('BookTitle', ''))
    else:
        data['title'] = su(book.get('BookTitle', ''))

    if book.get('Publisher', ''):
        data['publisher'] = book['Publisher'].get('PublisherName', '')
        data['pubplace'] = book['Publisher'].get('PublisherLocation', '')

    pubdate = book.get('PubDate', '')
    if pubdate:
        data['pubdate'] = cook_date_str(' '.join([i for i in (
            pubdate.get('Year', ''), pubdate.get('Season', ''),
            pubdate.get('Month', ''), pubdate.get('Day', '')) if i]))

    data['volume'] = book.get('Volume', '')
    data['volumetitle'] = book.get('VolumeTitle', '')
    data['edition'] = book.get('Edition', '')
    data['series'] = book.get('CollectionTitle', '')
    data['isbn'] = book.get('Isbn', '')
    if isinstance(data['isbn'], list):
        data['isbn'] = data['isbn'] and data['isbn'][0] or ''  # why does it do this?
    data['elocation'] = book.get('ELocationID', '')
    data['medium'] = book.get('Medium', '')
    data['reportnum'] = book.get('ReportNumber', '')

    # itemlist = document.get('ItemList','') - no idea what this is

    data['pmid'] = str(document['PMID'])

    sections = []
    for section in document.get('Sections', []):
        sec = dict()
        sec['title'] = section['SectionTitle']
        if section.get('LocationLabel', ''):
            sec['type'] = section['LocationLabel'].attributes['Type']
            sec['label'] = section['LocationLabel']
        else:
            sec['type'] = ''
            sec['label'] = ''
    data['sections'] = sections

    return data


def parse_entrez_journal_record(record):
    data = {'type': 'journal'}
    medline = record.pop('MedlineCitation')
    medlineinfo = medline.pop('MedlineJournalInfo')
    article = medline.pop('Article')
    journal = article.pop('Journal')
    pmdates = record['PubmedData'].pop('History')
    articleids = record['PubmedData'].pop('ArticleIdList')
    data['pubmodel'] = article.attributes['PubModel']
    articledate = article.pop('ArticleDate')

    data['journal'] = journal['Title']
    pubdate = journal['JournalIssue'].get('PubDate', {})
    data['volume'] = journal['JournalIssue'].get('Volume', '')
    data['issue'] = journal['JournalIssue'].get('Issue', '')

    data['medium'] = journal['JournalIssue'].attributes['CitedMedium']
    data['pagination'] = article.get('Pagination', {}).get('MedlinePgn', '')
    data['affiliation'] = article.get('Affiliation')
    data['pubdate'] = cook_date_str(' '.join([i for i in (
        pubdate.get('MedlineDate', ''), pubdate.get('Year', ''),
        pubdate.get('Season', ''), pubdate.get('Month', ''),
        pubdate.get('Day', '')) if i]))
    data['title'] = article['ArticleTitle']

    for pmdate in pmdates:
        pmdate_str = cook_date_str(
            ' '.join([i for i in (pmdate.get('Year', ''), pmdate.get('Month', ''), pmdate.get('Day', '')) if i]))
        data['pmpubdate_' + pmdate.attributes['PubStatus'].replace('-', '')] = pmdate_str

    authors = []
    for author in article.get('AuthorList', []):
        if author.attributes['ValidYN'] == 'Y':
            for aff in author.get('AffiliationInfo', []):
                data['affiliation'] = aff['Affiliation']
            authors.append({'lname': author.get('LastName', ''),
                            'fname': author.get('ForeName', ''),
                            'iname': author.get('Initials', ''),
                            'cname': author.get('CollectiveName', ''),
                            'suffix': author.get('Suffix', ''),
                            'investigator': False})
    for investigator in medline.get('InvestigatorList', []):
        if investigator.attributes['ValidYN'] == 'Y':
            authors.append({'lname': investigator.get('LastName', ''),
                            'fname': investigator.get('ForeName', ''),
                            'iname': investigator.get('Initials', ''),
                            'cname': investigator.get('CollectiveName', ''),
                            'suffix': investigator.get('Suffix', ''),
                            'investigator': True})
    data['authors'] = authors
    data['pmid'] = str(medline['PMID'])

    for aid in articleids:
        data[aid.attributes['IdType']] = unicode(aid)

    grants = []
    for grant in article.get('GrantList', []):
        grants.append({'grantid': grant.get('GrantID'),
                       'acronym': grant.get('Acronym'),
                       'agency': grant.get('Agency', '')})
    data['grants'] = grants
    mesh = []
    for meshHeader in medline.get('MeshHeadingList', []):
        mesh.append(unicode(meshHeader['DescriptorName']))
        # Might be nice to return name and ID at some point.
        # d = meshHeader['DescriptorName']
        # mesh.append({
        #    'name': unicode(d),
        #    'id': d.attributes['UI'],
        # })
    data['mesh'] = mesh
    data['pubtypelist'] = [unicode(ptl) for ptl in article.get('PublicationTypeList', [])]
    for adate in articledate:
        if adate.attributes['DateType'] == 'Electronic':
            data['edate'] = cook_date_str(' '.join([i for i in (
                adate.get('MedlineDate', ''), adate.get('Year', ''), adate.get('Season', ''),
                adate.get('Month', ''), adate.get('Day', '')) if i]))
    data['medlineta'] = medlineinfo.get('MedlineTA', '')
    data['nlmuniqueid'] = medlineinfo.get('NlmUniqueID', '')
    data['medlinecountry'] = medlineinfo.get('Country', '')
    data['medlinestatus'] = medline.attributes['Status']

    if article.get('Abstract'):
        _abstracts = []
        for abst in article['Abstract']['AbstractText']:
            text = unicode(abst)
            if hasattr(abst, 'attributes'):
                nlmcat = abst.attributes.get('NlmCategory')
                label = abst.attributes.get('Label')
            else:
                nlmcat = label = ''
            _abstracts.append({'text': text, 'nlmcategory': nlmcat, 'label': label})
        data['abstract'] = _abstracts

    data['pubstatus'] = record['PubmedData'].get('PublicationStatus', '')

    # dates
    for pmdate in record['PubmedData'].get('History', []):
        dtype = pmdate.attributes.get('PubStatus')
        _pmdate = ' '.join([d for d in (pmdate.get('Year'), pmdate.get('Month'), pmdate.get('Day')) if d])
        data['pmpubdate_%s' % dtype] = _pmdate

    return data


def get_publication(pmid):
    handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
    try:
        for rec in Entrez.parse(handle):
            return parse_entrez_record(rec)
    except ValueError:
        handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
        data = Entrez.read(handle)
        rec = None
        if data['PubmedArticle']:
            rec = parse_entrez_journal_record(data['PubmedArticle'][0])
        elif data['PubmedBookArticle']:
            rec = parse_entrez_book_record(data['PubmedBookArticle'][0])
        return rec
    finally:
        handle.close()


def get_publication_by_doi(doi):
    ids = find_publications(doi=doi)
    if int(ids['Count']) == 1:
        return get_publication(ids['IdList'][0])


def read_response(handle):
    """
    Fully reads a urlopen handle, taking into account IncompleteRead exceptions.
    """
    data = ''
    while True:
        try:
            data += handle.read()
            break
        except IncompleteRead as ir:
            data += ir.partial
    return data


def get_publications(pmids):
    """ We let Biopython do most of the heavy lifting, including building the request POST. Publications are
    fetched in chunks of config.MAX_PUBS as there does seem to be a limit imposed by NCBI. There is also
    a 3-request per second limit imposed by NCBI until we get an API key, but that should also be handled by
    Biopython. Finally, if the request fails for any reason we can retry config.MAX_RETRIES times

    :param pmids: a list of PMIDs
    :return: generator of pubs as python dicts
    """
    # Make sure pmids is a list, since that's what Entrez expects (and sets, for example, are not sliceable).
    total_time = time.time()
    if not isinstance(pmids, list):
        pmids = list(pmids)
    start = 0
    attempts = 0
    while start < len(pmids):
        pmid_slice = pmids[start:start + config.MAX_PUBS]
        try:
            timer = time.time()
            logger.info('Fetching publications %d through %d...' % (start, min(len(pmids),start+config.MAX_PUBS)))
            handle = Entrez.efetch(db="pubmed", id=pmid_slice, retmode="xml")
            data = Entrez.read(handle)
            logger.info('Fetched and read after %.02fs' % (time.time()-timer))
            for record in data['PubmedArticle'] + data['PubmedBookArticle']:
                yield parse_entrez_record(record)
            start += config.MAX_PUBS
            attempts = 0
        except Exception, e:
            attempts += 1
            logger.info('efetch failed: "%s", attempting retry %d' % (e,attempts))
            if attempts >= config.MAX_RETRIES:
                raise PubToolsError('Something is wrong with Entrez or these PMIDs: ' + ','.join(pmid_slice))
            time.sleep(config.RETRY_SLEEP)
        finally:
            handle.close()
    logger.info('Total publications retrieved in %.02f seconds' % (time.time()-total_time))


def find_pmids(query):
    handle = Entrez.esearch(db='pubmed', term=query, datetype='pdat', retmode='xml', retmax='100000')
    try:
        return Entrez.read(handle).get('IdList', [])
    finally:
        handle.close()


def get_searched_publications(WebEnv, QueryKey, ids=None):
    """ Get a bunch of publications from Entrez using WebEnv and QueryKey from EPost. Option to narrow
    down subset of ids """
    if isinstance(ids, basestring):
        ids = [ids]
    records = []
    query = {
        'db': 'pubmed',
        'webenv': WebEnv,
        'query_key': QueryKey,
        'retmode': 'xml'
    }
    if ids:
        query['ids'] = ids
    handle = Entrez.efetch(**query)
    try:
        for record in Entrez.parse(handle):
            record = parse_entrez_record(record)
            if record:
                records.append(record)
    except ValueError:  # newer Biopython requires this to be Entrez.read
        handle = Entrez.efetch(**query)
        data = Entrez.read(handle)
        for record in data['PubmedArticle'] + data['PubmedBookArticle']:
            record = parse_entrez_record(record)
            # Entrez.read does not use the ids query key so we have to do this ourselves
            if record and (ids and record['pmid'] in ids or not ids):
                records.append(record)
    return records


def esearch_publications(term):
    handle = Entrez.esearch(db="pubmed", term=term, datetype='pdat', retmode="xml", retmax="100000")
    return process_handle(handle)


def find_publications(authors=None, title=None, journal=None, start=None, end=None, pmid=None, mesh=None, gr=None,
                      ir=None, affl=None, doi='', inclusive=False):
    term = generate_search_string(authors, title, journal, pmid, mesh, gr, ir, affl, doi, inclusive)
    if not start:
        start = '1500/01/01'
    if not end:
        end = '2099/01/01'
    handle = Entrez.esearch(db="pubmed", term=term, datetype='pdat', mindate=start, maxdate=end, retmode="xml",
                            retmax="100000")
    return process_handle(handle)


def process_handle(handle):
    record = Entrez.read(handle)
    if record['IdList']:
        # If we have search results, send the ids to EPost and use WebEnv/QueryKey from now on
        search_results = Entrez.read(Entrez.epost("pubmed", id=",".join(record['IdList'])))
        record['WebEnv'] = search_results['WebEnv']
        record['QueryKey'] = search_results['QueryKey']
    return record


def generate_search_string(authors, title, journal, pmid, mesh, gr, ir, affl, doi, inclusive=False):
    """Generate the search string that will be passed to ESearch based on these criteria"""
    authjoin = inclusive == "OR" and " OR " or " "
    authors_string = authors and authjoin.join(['%s[auth]' % unidecode(a) for a in authors if a]) or ''
    stops = ['a', 'about', 'again', 'all', 'almost', 'also', 'although', 'always', 'among', 'an', 'and', 'another',
             'any',
             'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'between', 'both', 'but', 'by', 'can',
             'could',
             'did', 'do', 'does', 'done', 'due', 'during', 'each', 'either', 'enough', 'especially', 'etc', 'for',
             'found',
             'from', 'further', 'had', 'has', 'have', 'having', 'here', 'how', 'however', 'i', 'if', 'in', 'into', 'is',
             'it',
             'its', 'itself', 'just', 'kg', 'km', 'made', 'mainly', 'make', 'may', 'mg', 'might', 'ml', 'mm', 'most',
             'mostly',
             'must', 'nearly', 'neither', 'no', 'nor', 'obtained', 'of', 'often', 'on', 'our', 'overall', 'perhaps',
             'quite',
             'rather', 'really', 'regarding', 'seem', 'seen', 'several', 'should', 'show', 'showed', 'shown', 'shows',
             'significantly', 'since', 'so', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'then',
             'there', 'therefore', 'these', 'they', 'this', 'those', 'through', 'thus', 'to', 'upon', 'use', 'used',
             'using',
             'various', 'very', 'was', 'we', 'were', 'what', 'when', 'which', 'while', 'with', 'within', 'without',
             'would']
    pstops = ['\&', '\(', '\)', '\-', '\;', '\:', '\,', '\.', '\?', '\!', ' ']
    if title:
        for stop in stops:
            comp = re.compile(r'(\s)?\b%s\b(\s)?' % stop, re.IGNORECASE)
            title = comp.sub('*', title)
        for stop in pstops:
            comp = re.compile(r'(\s)?(\b)?%s(\b)?(\s)?' % stop, re.IGNORECASE)
            title = comp.sub('*', title)
        titlevals = [elem.strip() for elem in title.split('*')]
        title_string = titlevals and '+'.join(['%s[titl]' % unidecode(t) for t in titlevals if t]) or ''
    else:
        title_string = ''
    journal_string = journal and '"%s"[jour]' % unidecode(journal) or ''
    pmid_string = pmid and '%s[pmid]' % pmid or ''
    gr_string = gr and '%s[gr]' % gr or ''
    affl_string = affl and '%s[affl]' % affl or ''
    ir_string = ir and '%s[ir]' % ir or ''
    mesh_string = mesh and '+'.join(['%s[mesh]' % m for m in mesh]) or ''
    doi_string = doi and '%s[doi]' % doi.replace('(', ' ').replace(')', ' ') or ''

    return '+'.join([elem for elem in (
        authors_string, title_string, journal_string, pmid_string, mesh_string, gr_string, ir_string, affl_string,
        doi_string) if elem])
