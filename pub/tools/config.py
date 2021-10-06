import os

ENTREZ_TOOL = "pub.tools"
ENTREZ_EMAIL = os.environ.get('ENTREZ_EMAIL')  # "plone.administration@imsweb.com"
ENTREZ_API_KEY = os.environ.get('ENTREZ_API_KEY')  # ''
NO_VALUE = "<<blank>>"
MAX_PUBS = 9000
# Biopython will put a count greater than 200 ids into a post, so we don't need to worry about request size
# But there does seem to be a 9999 limit either from Biopython or from NCBI
MAX_RETRIES = 3
RETRY_SLEEP = 0.25
