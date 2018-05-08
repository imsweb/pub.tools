# Changes to pub.tools

## [1.7] - 10 May 2018
- Refactor some entrez functions to make it more obvious what the API endpoints are
- Convert docstring of all intended end point functions to reST
- Add ability to find publication by PMC ID. This is done by querying the PMC database
- Refactor generate_search_query slightly

## [1.6] - 1 March 2018
- Fixed the book REST API calls to allow for failure
- book REST API calls now use requests module
- the isbndb.com database is now a paid service only. It *should* work but I don't have a service to verify this

## [1.5]
- Citations can now be generated as plain text without <i> tags on journals, etc. It defaults to true
here but will default to false in a future release.
- Removed some unused parameters from citation functions
- Cleaned up unit tests
- Fixed issue with eCollection dates in citations

## [1.4]
- Refactor and reformat for pep8