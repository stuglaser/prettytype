Pretty-printer for complex python types
=======================================

This package helps describe complex, nested Python data structures. Use the
``prettytype`` function to print the structure and quickly understand what type of
object you have.

Install with: ``pip install prettytype``

For example, let's examine a complex JSON object from the internet:

.. code:: python

    import requests
    import json
    
    r = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:0385472579,LCCN:62019420&format=json')
    data = json.loads(r.text)
    print 'Data:', data
    print
    
    from prettytype import prettytype
    print 'Type:', prettytype(data)
    
    ===>

    Data: {u'ISBN:0385472579': {u'bib_key': u'ISBN:0385472579', ......
    
    Type: {str: {str: str}}

prettytype shows that the API returns nested dictionaries with string keys.
