Pretty-printer for complex python types
=======================================

This package helps describe complex, nested Python data structures. Use the
`prettytype` function to print the structure and quickly understand what type of
object you have.

For example, let's examine a complex JSON object from the internet:

```
import requests
import json

r = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:0385472579,LCCN:62019420&format=json')
data = json.loads(r.text)
print 'Data:', data
print

from prettytype import prettytype
print 'Type:', prettytype(data)

===>
Data: {u'ISBN:0385472579': {u'bib_key': u'ISBN:0385472579', u'preview': u'noview', u'thumbnail_url': u'https://covers.openlibrary.org/b/id/240726-S.jpg', u'preview_url': u'https://openlibrary.org/books/OL1397864M/Zen_speaks', u'info_url': u'https://openlibrary.org/books/OL1397864M/Zen_speaks'}, u'LCCN:62019420': {u'bib_key': u'LCCN:62019420', u'preview': u'noview', u'preview_url': u'https://openlibrary.org/books/OL5857365M/The_adventures_of_Tom_Sawyer', u'info_url': u'https://openlibrary.org/books/OL5857365M/The_adventures_of_Tom_Sawyer'}}

Type: {str: {str: str}}
```

prettytype shows that the API returns nested dictionaries with string keys.
