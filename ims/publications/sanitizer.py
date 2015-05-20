from config import NO_VALUE

def su(value, encoding='utf-8'):
    """Converts a value to unicode, even it is already a unicode string."""
    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        try:
            value = unicode(value, encoding)
        except (UnicodeDecodeError):
            value = value.decode('utf-8', 'replace')
    return value


punclist = ['.',',',':',';','\'','(',')','{','}','[',']','=','+','$','#','%','@','!','^','&','*']

def sanitize(datastring):
  return su(datastring)

def blankify(datastring=''):
  return datastring or NO_VALUE

def depunctuate(datastring):
  return datastring and ''.join([char for char in datastring if char not in punclist]) or ''