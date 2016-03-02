import csv
import json
import os
import urllib2

base_path = os.path.dirname(os.path.realpath(__file__))

# cache journal info on start up


def cache():
    url = 'http://www.ncbi.nlm.nih.gov/pmc/front-page/NIH_PA_journal_list.csv'
    try:
        conn = urllib2.urlopen(url)
        reader = csv.reader(conn)

        atoj = {}
        jtoa = {}
        dates = {}
        while True:
            try:
                title, abbr, pissn, eissn, start, end = reader.next()
                atoj[abbr.lower()] = title
                jtoa[title.lower()] = abbr
                dates[abbr.lower()] = (start, end)
            except StopIteration:
                break
        data = {'atoj': atoj, 'jtoa': jtoa, 'dates': dates}

        f = open(os.path.join(base_path, 'journals.json'), 'w')
        json.dump(data, f)
        f.close()
    except urllib2.HTTPError:
        pass


def get_abbreviations():
    f = open(os.path.join(base_path, 'journals.json'))
    return json.load(f)['atoj']


def get_journals():
    f = open(os.path.join(base_path, 'journals.json'))
    return json.load(f)['jtoa']


def atoj(abbrv):
    data = get_abbreviations()
    return data.get(abbrv.lower())


def jtoa(journal):
    data = get_journals()
    return data.get(journal.lower())


def atodates(abbrv):
    f = open(os.path.join(base_path, 'journals.json'))
    data = json.load(f)['dates']
    return data.get(abbrv.lower())

try:
    cache()
except urllib2.URLError:  # if ncbi is down
    pass
