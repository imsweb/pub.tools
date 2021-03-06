# Changelog

## [3.0.1] - 22 Aug 2019
- journals module reconfigured to not write to disk on startup

## [3.0] - 12 Aug 2019
- Exlusively supports python 3

## [2.1] - unreleased
- Redesign of citation with abstract behavior.
- "italicize" option has been replaced with an "html" option and does not do any safe escape
- add docstrings to citation functions

## [2.0.2] - 25 Jan 2019
- Revert safe_unicode use but have it be only applicable for python 2. Not an issue in python 3
- Unescape all fields except title and abstract if using the "escape" parameter. Those two fields are treated as HTML 
if escape is false all other fields are plain text 

## [2.0] - 17 October 2018
- Six implementation with support for python 2 and 3 [hoskins]

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