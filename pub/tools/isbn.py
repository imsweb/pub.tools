from elementtree import ElementTree as et
import json, re, urllib2

from cooking import alphanum, cookDateStr, su

class IsbnData(object):
  book_title = u''
  language = u''
  publisher = u''
  authors = []
  editors = []
  abstract = u''
  pubdate = u''
  google_books_link = u''

  def get(self, key): # dict like
    if hasattr(self, key):
      return self[key]

  def __getitem__(self, key): # dict like
    return getattr(self, key)

  def __setitem__(self, key, value): # dict like
    return setattr(self, key, value)

class IsbnOpener(object):
  root_url = '' # for construction
  url = '' # for displays
  name = 'Default opener'
  def __init__(self, api_key=None):
    self.api_key = api_key

  def get_publication(self, isbn):
    """ Should always return an IsbnData object """
    return IsbnData()

class IsbnDbOpener(IsbnOpener):
  root_url = 'http://isbndb.com/api/v2/json/%(api_key)s/%(endpoint)s/%(term)s'
  name = 'ISBNdb'

  def url(self, term):
    return self.root_url % {'api_key': self.api_key,
                            'endpoint': 'book',
                            'term': term}

  def get_url(self, endpoint, term):
    handle = urllib2.urlopen(self.root_url % {'api_key': self.api_key,
                            'endpoint': endpoint,
                            'term': term})
    return json.load(handle)

  def get_publication(self, isbn):
    data = IsbnData()
    isbn = alphanum(isbn)
    book = self.get_url(endpoint='book',term=isbn)
    if book.get('data'):
      book = book['data'][0]
      data['title'] = su(book.get('title_long') or book.get('title'))
      data['language'] = book.get('language')
      data['authors'] = [b.get('name_latin') or b['name'] for b in book.get('author_data')]
      data['publisher'] = book.get('publisher_name')
      data['abstract'] = book['summary']
      return data

class GoogleBooksAPIOpener(IsbnOpener):
  root_url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:%(isbn)s&key=%(api_key)s'
  name = 'Google Books API'

  def url(self, isbn):
    return self.root_url % {'api_key': self.api_key,
                            'isbn': isbn}

  def get_url(self, isbn):
    handle = urllib2.urlopen(self.url(isbn))
    return json.load(handle)

  def get_publication(self, isbn):
    data = IsbnData()
    isbn = alphanum(isbn)
    book = self.get_url(isbn)
    if book['totalItems']:
      book = book['items'][0]['volumeInfo']
      data['title'] = book['title']
      data['language'] = book.get('language')
      data['authors'] = book.get('authors') or []
      data['publisher'] = book.get('publisher')
      data['abstract'] = book.get('description')
      if book.get('publishedDate'):
        data['pubdate'] = cookDateStr(book['publishedDate'])
      data['google_books_link'] = book['previewLink']
      return data

class WorldCatOpener(IsbnOpener):
  root_url = 'http://classify.oclc.org/classify2/Classify?isbn=%(isbn)s&summary=true'
  name = 'WorldCat'

  def url(self, term):
    return self.root_url % {'isbn':term}

  def get_url(self, isbn):
    handle = urllib2.urlopen(self.root_url % {'isbn':isbn})
    return handle

  def get_publication(self, isbn):
    data = IsbnData()
    isbn = alphanum(isbn)
    source = self.get_url(isbn)

    tree = et.parse(source)
    ns = 'http://classify.oclc.org'

    authors = []
    editors = []
    root = tree.getroot()
    _authors = root.find('{%s}%s' % (ns,'authors'))
    if _authors:
      for author in _authors.findall('{%s}%s' % (ns,'author')):
        author = author.text
        brkt_pattern = '\[(.*?)\]'
        brkt = re.search(brkt_pattern, author)
        if brkt:
          brkt_value = brkt.group(1)
          author_name = author.split(brkt.group())[0].strip()
          # what values are allowed here? Just try for editor for now
          for role in brkt_value.split(';'):
            role = role.strip()
            if role == 'Editor' and author_name not in editors:
              editors.append(author_name)
            elif role == 'Author' and author_name not in authors:
              authors.append(author_name)
        else:
          authors.append(author)
      data['authors'] = authors
      data['editors'] = editors
      data['title'] = ''
      data['title'] = root.find('{%s}%s' % (ns,'work')).attrib['title']
      return data