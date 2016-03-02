from . import config
from .cooking import cookDateStr, su
from Bio import Entrez
from math import ceil
from unidecode import unidecode
import re

Entrez.email = config.ENTREZ_EMAIL
Entrez.tool = config.ENTREZ_TOOL

class IMSEntrezError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

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
    data = {'type':'book'}
    document = record.pop('BookDocument')
    book = document.pop('Book')
    # publicationtype = document.pop('PublicationType') - unsure what this is
    # kwlist = document.pop('KeywordList') - unsure what this is

    authors = []
    if document.get('AuthorList', []) and document['AuthorList'][0].attributes['Type'] == 'authors':
        for author in document['AuthorList'][0]:
            for aff in author.get('AffiliationInfo', []):
                data['affiliation'] = aff['Affiliation']
            authors.append({'lname':author.get('LastName', ''),
                            'fname':author.get('ForeName', ''),
                            'iname':author.get('Initials', ''),
                            'cname':author.get('CollectiveName', ''),
                            'suffix':author.get('Suffix', ''),
                            'investigator':False})
    data['authors'] = authors

    editors = []
    if book.get('AuthorList', []) and book['AuthorList'][0].attributes['Type'] == 'editors':
        for author in book['AuthorList'][0]:
            for aff in author.get('AffiliationInfo', []):
                data['affiliation'] = aff['Affiliation']
            authors.append({'lname':author.get('LastName', ''),
                            'fname':author.get('ForeName', ''),
                            'iname':author.get('Initials', ''),
                            'cname':author.get('CollectiveName', ''),
                            'suffix':author.get('Suffix', ''),
                            'investigator':False})
    data['editors'] = editors

    data['language'] = document.get('Language', '') and document['Language'][0]

    articleids = document.pop('ArticleIdList')
    for aid in articleids:
        data[ aid.attributes['IdType'] ] = unicode(aid)

    data['abstract'] = document.get('Abstract', {}).get('AbstractText', '')
    if isinstance(data['abstract'], list):
        data['abstract'] = data['abstract'][0] # why does it do this?
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
        data['pubdate'] = cookDateStr(' '.join([i for i in (pubdate.get('Year', ''), pubdate.get('Season', ''), pubdate.get('Month', ''), pubdate.get('Day', '')) if i]))

    data['volume'] = book.get('Volume', '')
    data['volumetitle'] = book.get('VolumeTitle', '')
    data['edition'] = book.get('Edition', '')
    data['series'] = book.get('CollectionTitle', '')
    data['isbn'] = book.get('Isbn', '')
    if isinstance(data['isbn'], list):
        data['isbn'] = data['isbn'] and data['isbn'][0] or ''# why does it do this?
    data['elocation'] = book.get('ELocationID', '')
    data['medium'] = book.get('Medium', '')
    data['reportnum'] = book.get('ReportNumber', '')

    # itemlist = document.get('ItemList','') - no idea what this is

    data['pmid'] = str(document['PMID'])

    sections = []
    for section in document.get('Sections', []):
        sec = {}
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
    data = {'type':'journal'}
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
    data['pubdate'] = cookDateStr(' '.join([i for i in (pubdate.get('MedlineDate', ''), pubdate.get('Year', ''), pubdate.get('Season', ''), pubdate.get('Month', ''), pubdate.get('Day', '')) if i]))
    data['title'] = article['ArticleTitle']

    for pmdate in pmdates:
        pmdate_str = cookDateStr(' '.join([i for i in (pmdate.get('Year', ''), pmdate.get('Month', ''), pmdate.get('Day', '')) if i]))
        data['pmpubdate_' + pmdate.attributes['PubStatus'].replace('-', '')] = pmdate_str

    authors = []
    for author in article.get('AuthorList', []):
        if author.attributes['ValidYN'] == 'Y':
            for aff in author.get('AffiliationInfo', []):
                data['affiliation'] = aff['Affiliation']
            authors.append({'lname':author.get('LastName', ''),
                            'fname':author.get('ForeName', ''),
                            'iname':author.get('Initials', ''),
                            'cname':author.get('CollectiveName', ''),
                            'suffix':author.get('Suffix', ''),
                            'investigator':False})
    for investigator in medline.get('InvestigatorList', []):
        if investigator.attributes['ValidYN'] == 'Y':
            authors.append({'lname':investigator.get('LastName', ''),
                            'fname':investigator.get('ForeName', ''),
                            'iname':investigator.get('Initials', ''),
                            'cname':investigator.get('CollectiveName', ''),
                            'suffix':investigator.get('Suffix', ''),
                            'investigator':True})
    data['authors'] = authors
    data['pmid'] = str(medline['PMID'])

    for aid in articleids:
        data[ aid.attributes['IdType'] ] = unicode(aid)

    grants = []
    for grant in article.get('GrantList', []):
        grants.append({'grantid':grant.get('GrantID'),
                       'acronym':grant.get('Acronym'),
                       'agency':grant.get('Agency', '')})
    data['grants'] = grants
    mesh = []
    for meshHeader in medline.get('MeshHeadingList', []):
        mesh.append(unicode(meshHeader['DescriptorName']))
        # Might be nice to return name and ID at some point.
        #d = meshHeader['DescriptorName']
        #mesh.append({
        #    'name': unicode(d),
        #    'id': d.attributes['UI'],
        #})
    data['mesh'] = mesh
    data['pubtypelist'] = [unicode(ptl) for ptl in article.get('PublicationTypeList', [])]
    for adate in articledate:
        if adate.attributes['DateType'] == 'Electronic':
            data['edate'] = cookDateStr(' '.join([i for i in (adate.get('MedlineDate', ''), adate.get('Year', ''), adate.get('Season', ''), adate.get('Month', ''), adate.get('Day', '')) if i]))
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
            _abstracts.append({'text':text, 'nlmcategory':nlmcat, 'label':label})
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
    finally:
        handle.close()

def get_publication_by_doi(doi):
    ids = find_publications(doi=doi)
    if int(ids['Count']) == 1:
        return get_publication(ids['IdList'][0])

def get_publications(pmids):
    # Make sure pmids is a list, since that's what Entrez expects (and sets, for example, are not sliceable).
    if not isinstance(pmids, list):
        pmids = list(pmids)
    # We don't need to enforce the three-queries rule because biopython does that
    # But we do need to prevent the URL from getting too long
    publen = len(pmids)
    # cap is ~4096 but about 150 other chars
    # an 8-character pmid +3 (comma=%2c) ~= (4096-150)/(8+3) ~= 358
    for counter in range(0, int(ceil(publen / float(config.MAX_PUBS)))):
        lowend = counter * config.MAX_PUBS
        topend = (counter + 1) * config.MAX_PUBS
        if topend > publen:
            topend = publen
        handle = Entrez.efetch(db="pubmed", id=pmids[lowend:topend], retmode="xml")

        #try:
        for record in Entrez.parse(handle):
            yield parse_entrez_record(record)
        #except:
        #  raise Exception('Something is wrong with Entrez or these PMIDs: ' + ','.join(pmids[lowend:topend]))
        handle.close()

def find_pmids(query):
    handle = Entrez.esearch(db='pubmed', term=query, datetype='pdat', retmode='xml', retmax='100000')
    try:
        return Entrez.read(handle).get('IdList', [])
    finally:
        handle.close()

def get_searched_publications(WebEnv, QueryKey, ids=None):
    """ Get a bunch of publications from Entrez using WebEnv and QueryKey from EPost. Option to narrow down subset of ids """
    records = []
    if ids:
        handle = Entrez.efetch(db="pubmed", webenv=WebEnv, query_key=QueryKey, id=ids, retmode="xml")
    else:
        handle = Entrez.efetch(db="pubmed", webenv=WebEnv, query_key=QueryKey, retmode="xml")
    for record in Entrez.parse(handle):
        record = parse_entrez_record(record)
        if record:
            records.append(record)
    return records

def esearch_publications(term):
    handle = Entrez.esearch(db="pubmed", term=term, datetype='pdat', retmode="xml", retmax="100000")
    return process_handle(handle)

def find_publications(authors=None, title=None, journal=None, start=None, end=None, pmid=None, mesh=None, gr=None, ir=None, affl=None, doi=False, inclusive=False):
    term = generate_search_string(authors, title, journal, pmid, mesh, gr, ir, affl, doi, inclusive)
    if not start:
        start = '1500/01/01'
    if not end:
        end = '2099/01/01'
    handle = Entrez.esearch(db="pubmed", term=term, datetype='pdat', mindate=start, maxdate=end, retmode="xml", retmax="100000")
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
    stops = ['a', 'about', 'again', 'all', 'almost', 'also', 'although', 'always', 'among', 'an', 'and', 'another', 'any',
             'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'between', 'both', 'but', 'by', 'can', 'could',
             'did', 'do', 'does', 'done', 'due', 'during', 'each', 'either', 'enough', 'especially', 'etc', 'for', 'found',
             'from', 'further', 'had', 'has', 'have', 'having', 'here', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it',
             'its', 'itself', 'just', 'kg', 'km', 'made', 'mainly', 'make', 'may', 'mg', 'might', 'ml', 'mm', 'most', 'mostly',
             'must', 'nearly', 'neither', 'no', 'nor', 'obtained', 'of', 'often', 'on', 'our', 'overall', 'perhaps', 'quite',
             'rather', 'really', 'regarding', 'seem', 'seen', 'several', 'should', 'show', 'showed', 'shown', 'shows',
             'significantly', 'since', 'so', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'then',
             'there', 'therefore', 'these', 'they', 'this', 'those', 'through', 'thus', 'to', 'upon', 'use', 'used', 'using',
             'various', 'very', 'was', 'we', 'were', 'what', 'when', 'which', 'while', 'with', 'within', 'without', 'would']
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

    return '+'.join([elem for elem in (authors_string, title_string, journal_string, pmid_string, mesh_string, gr_string, ir_string, affl_string, doi_string) if elem])
