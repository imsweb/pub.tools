from . import config
from datetime import datetime

preferred_date_format = '%Y %b %d'
preferred_date_format_long = '%Y %b %d %I:%M %p'

mmap = {'winter':1, 'spring':4, 'summer':7, 'fall':10, 'autumn':10, 'win':1, 'spr':4, 'sum':7, 'fal':10, 'aut':10,
    'jan':1, 'january':1, 'feb':2, 'february':2, 'mar':3, 'march':3, 'apr':4, 'april':4, 'may':5, 'jun':6, 'june':6,
    'jul':7, 'july':7, 'aug':8, 'august':8, 'sep':9, 'september':9, 'oct':10, 'october':10, 'nov':11, 'november':11,
    'dec':12, 'december':12, '1stquart':1, '2ndquart':4, '3rdquart':7, '4thquart':10}
mmap_end = {'winter':3, 'spring':6, 'summer':9, 'fall':12, 'autumn':12, 'win':3, 'spr':6, 'sum':9, 'fal':12, 'aut':12,
    'jan':1, 'january':1, 'feb':2, 'february':2, 'mar':3, 'march':3, 'apr':4, 'april':4, 'may':5, 'jun':6, 'june':6,
    'jul':7, 'july':7, 'aug':8, 'august':8, 'sep':9, 'september':9, 'oct':10, 'october':10, 'nov':11, 'november':11,
    'dec':12, 'december':12, '1stquart':3, '2ndquart':6, '3rdquart':9, '4thquart':12}
rmap = {'winter':'Winter', 'spring':'Spring', 'summer':'Summer', 'fall':'Fall', 'autumn':'Autumn', 'win':'Win',
    'spr':'Spr', 'sum':'Sum', 'fal':'Fal', 'aut':'Aut', 'jan':'Jan', 'january':'Jan', 'feb':'Feb', 'february':'Feb',
    'mar':'Mar', 'march':'Mar', 'apr':'Apr', 'april':'Apr', 'may':'May', 'jun':'Jun', 'june':'Jun', 'jul':'Jul',
    'july':'Jul', 'aug':'Aug', 'august':'Aug', 'sep':'Sep', 'september':'Sep', 'oct':'Oct', 'october':'Oct',
    'nov':'Nov', 'november':'Nov', 'dec':'Dec', 'december':'Dec'}
rism = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09',
    'Oct':'10', 'Nov':'11', 'Dec':'12'}
monthlist = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
punclist = ['.', ',', ':', ';', '\'', '(', ')', '{', '}', '[', ']', '=', '+', '$', '#', '%', '@', '!', '^', '&', '*']

def cookDate(year='', month='', day='', medlinedate='', end=False):
    """ returns a datetime object
        medlinedate:
           - string containing the full date
           - used by PubMed (medline) to represent atypical dates, like Spring 2008
           - takes precedence over year/month/day values
        end:
          - if the result represents a date range we return the start unless this variable is true
    """

    if medlinedate:
        medlinedate = medlinedate.replace(' Quart', 'Quart')
        if ' ' in medlinedate:
            medlinedate = medlinedate.replace('/', '-').replace(',', '').strip()
        else:
            medlinedate = medlinedate.replace('/', ' ').replace(',', '').strip()
        vals = medlinedate.split(' ')
        if len(vals) == 2: # year/month or month/year
            if ord(vals[0][0]) in range(48, 58): # year/month
                year = vals[0]
                month = vals[1]
            else: # month/year
                year = vals[1]
                month = vals[0]
            if not end:
                year = year.split('-')[0]
            else:
                year = year.split('-')[-1]
        elif len(vals) == 3: # day / month / year
            try:
                if not end:
                    day = vals[0].split('-')[0]
                else:
                    day = vals[0].split('-')[-1]
                month = vals[1]
                year = vals[2].split('-')[0]
                if len(month.split('-')) > 1 and ord(month.split('-')[1][0]) in range(48, 58):
                    if not end:
                        vals = medlinedate.split('-')[0]
                    else:
                        vals = medlinedate.split('-')[-1]
                    year = vals.split(' ')[0]
                    month = vals.split(' ')[1]
                    day = 1
                elif int(year) < 32:
                    holder = day
                    day = year
                    year = holder
            except:
                import pdb; pdb.set_trace()
        else:
            if not end:
                year = vals[0].split('-')[0]
            else:
                year = vals[0].split('-')[-1]
    try:
        month = int(month)
    except (ValueError, TypeError,):
        if not end:
            month = mmap.get(str(month.lower()).split('-')[0], 1)
        else:
            month = mmap_end.get(str(month.lower()).split('-')[-1], 1)
    if not day:
        day = 1
    cooked = datetime(int(year), int(month), int(day))
    return cooked

def cookDateStr(value):
    """ takes a string and reformats it to '%Y %b %-d'. e.g. '8-11-2009' becomes '2009 Aug 11'
    """
    try:
        value = value.replace('th ', ' ').replace('nd ', ' ').replace('st ', ' ')
        if '- ' in value:
            value = value.replace(' - ', '-').replace('- ', '-')
        if not ' ' in value:
            value = value.replace('-', ' ')
        else:
            value = value.replace('/', '-')
        value = value.replace('/', ' ').replace(',', '')
        vals = value.split(' ')
        year = month = day = ''
        # 2006 Dec-2007 Jan
        if len(vals) == 3 and len(vals[1].split('-')) > 1 and ord(vals[1].split('-')[1][0]) in range(48, 58):
            year = vals[0]
            month = vals[1].split('-')[0]
        else:
            for val in vals:
                try:
                    num = int(val)
                except ValueError: #string, month/season
                    if month:
                        day = mmap[month.lower()]
                    month = '-'.join([rmap[m.lower()] for m in val.split('-') if m])
                    continue
                if num > 12 and num < 32:
                    if day:
                        month = monthlist[day - 1]
                        day = num
                    else:
                        day = num
                elif num < 13:
                    if month:
                        day = num
                    else:
                        month = monthlist[num - 1]
                elif num > 31:
                    year = num
        return ' '.join([str(i) for i in (year, month, day) if i])
    except KeyError:
        return value

def cookDateRIS(value):
    """ converts a string representing a date into RIS format
    """
    value = cookDateStr(value)
    vals = value.split(' ')
    year = month = other = day = ''
    if vals:
        year = vals[0]
    if len(vals) > 1:
        if rism.get(vals[1]):
            month = rism[vals[1]]
        else:
            other = vals[1]
    if len(vals) > 2:
        try:
            day = '%02d' % int(vals[2])
        except ValueError:
            day = vals[2]
    year = year.split('-')[0]
    month = month.split('-')[0]
    day = day.split('-')[0]
    return '/'.join([i for i in (year, month, day, other)])

def cookDateMonths(start, end):
    """ returns a list of all months within the date range. Useful for list based searches
    """
    months = []
    years = range(start.year, end.year + 1)
    for year in years:
        month_start = 1
        month_end = 13
        if year == start.year:
            month_start = start.month
        if year == end.year:
            month_end = end.month + 1
        for month in range(month_start, month_end):
            months.append(monthlist[month - 1] + ' ' + str(year))
    return months

def su(value, encoding='utf-8'):
    """ Converts a value to unicode, even it is already a unicode string.
    """
    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        try:
            value = unicode(value, encoding)
        except (UnicodeDecodeError):
            value = value.decode('utf-8', 'replace')
    return value

def sanitize(datastring):
    import warnings
    warnings.warn("pub.tools.sanitize is deprecated in favor of pub.tools.su", DeprecationWarning)
    return su(datastring)

def blankify(datastring=''):
    """ If the value is blank we'll return a non-blank value meant to represent a null value
        This allows us to search on that value
    """
    return datastring or config.NO_VALUE

def depunctuate(datastring):
    """ Remove punctuation
    """
    return datastring and ''.join([char for char in datastring if char not in punclist]) or ''
