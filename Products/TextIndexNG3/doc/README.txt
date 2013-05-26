===========================================================================
TextIndexNG V 3 - A fulltext indexing solution for Zope 2, Plone and Zope 3
===========================================================================

.. note:: **For upgraders**: existing indexes (existing pre-V 3.3.0 indexes)
           must be **cleared** within the ZMI of your catalog. 

           They **must** **not be removed** - 

           Clearing the indexes should be enough!!!

What is TextIndexNG V3?
=======================

TXNG 3 is the reimplementation of the well-known TextIndexNG product for 
Zope 2 using Zope 3 technologies. The current implementation runs
out-of-the-box on Zope 2 (in combination with Five). The core implementation
can be re-used easily in Zope 3.


Features
========

- multiple-field indexing (e.g. you can create one index to index content
  by title, author and body and perform queries against each field)

- multi-lingual support  (Products.LinguaPlone and plone.app.multilingual)

- pluggable components (storages, lexicons, query parsers, splitters, 
  stopwords, normalizers) 

- complex queries (AND, OR, NOT, phrase search, right truncation, wildcards,
  similarity search)

- indexes foreign formats (DOC, PDF, XML, SGML, PPT etc.)

- optional query autoexpansion to improve search results


Requirements
============

- Zope 2.10+

- for running TextIndexNG3 with Plone, you need Plone 3.1 or higher 


Download and project area
=========================

TextIndexNG 3 is currently hosted on Github:
   
    https://github.com/zopyx/Products.TextIndexNG3

Support
=======

  Bugs, support issues are handled for free ``soley`` either through the
  TextIndexNG 3 bugtracker on Github:

    https://github.com/zopyx/Products.TextIndexNG3/issues


  Dedicated commercial support is available on a per-hour or per-issue basis
  from http://www.zopyx.com/. 

  The latest source code is available from Github

    https://github.com/zopyx/Products.TextIndexNG3


License
=======

TextIndexNG 3 is published under the Zope Public License V 2.1 (see ZPL.txt)
Other license agreements can be made. Contact us for details (info@zopyx.com).

TextIndexNG 3 contains copies of ZCTextIndex/WidCopy.py and ZCTextIndex/NBest.py
which are published under the Zope Public License ZPL.

TextIndexNG 3 ships with a copy of the Snowball code (snowball.tartarus.org)
for implementing stemming. This code is (C) 2001, Dr. Martin Porter and
published under the BSD license.

TextIndexNG3 ships with a modified version of PLY, (C) 2001, David M.
Beazley. PLY is published under the GNU Lesser Public License (LGPL).

TextIndexNG3 ships with the python-levenshtein extension written by
David Necas und published under the GNU Public License (GPL).


Credits
=======

Many thanks to Yvo Schubbe for contributing a lot of code for the 3.2.0
release.  Thanks to Christian Zagrodnik for working on the 3.4.0 release.


Contributions
=============

Third-party contributions that become part of the TextIndexNG3 core (means they
are being checked into the TextIndexNG3 source repository) must be made under
the same license as the source (ZPL 2.1). Contributed code is subject to be
relicensed without further notice of the orginal contributor.


Installation
============

Installation with zc.buildout
-----------------------------

- starting TextIndexNG3 3.3.0 the only supported and recommended
  way to install TextIndexNG3 using ``zc.buildout``. Add::

      eggs = Products.TextIndexNG3

  to your ``buildout.cfg`` file.

  Compiling and installing the extension modules requires a C compiler
  (usually GCC on Unix systems works perfectly). On Windows systems you need
  Visual C++ to compile the extension modules. 

Installation on Plone
---------------------

- follow the steps above

- go to "Plone setup" -> "Add/remove programs"

- choose TextIndexNG3 to be added as new product

- a new configlet for TextIndexNG3 will appear on the setup screen (left
  side)

- click on the configlet and choose the only option to replace the
  existing index setup with TextIndexNG3 indexes

- that's it  


External converters
===================


To convert foreign formats like .doc, .pdf etc. you need to install
some external converters. See 

    http://zopyx.com/projects/TextIndexNG3/documentation

for details.
    

How to make your custom content-types searchable
================================================

Most current Zope index implementations are built on the fact that an
index with id XX tries to lookup the indexable content either from an objects
XX attribute or by calling the method XX() of the object. Although TextIndexNG
V3 still supports this behaviour, the recommended way to make custom types
indexable through TXNG3 is through providing dedicated methods that return
indexable content. The API of these methods is defined in
src/textindexng/interfaces/indexable.py. Custom types must either implement the
IIndexableContent API directly or provide the interface through an adapter
registered through ZCML. The IndexContentCollector class should be used to
return indexable content either as unicode string or as binary stream (to be
transformed through external converters). Some example how to use the 
indexing API can be found in src/textindexng/tests/mock.py (see classes
Mock, MockPDF and StupidMockAdapter)


How to query the index?
=======================

TextIndexNG accepts multiple query options that influence the search
results (options passed to the search() method):

- `query` - the search query (see below). Warning: the search query
  must *always* be a Python unicode string

- `parser`  - id of a registered parser (default: txng.parsers.english)

- `language` - *one* of the languages registered for a particular index
  (default: the *first* registered language)

- `field` - perform query against this field (as registered with the index)

- `similarity_ratio` - a float value between 0.0 and 1.0 to determine the
  ratio for measuring the similarity of terms based on the Levenshtein distance
  (default: 0.75)

- `autoexpand` - 'off'|'always'|'on_miss' (default: 'off') determines how
  query terms are treated. 'on_miss' expands the query terms to all terms that
  are similiar to the original search term (if could not be found).  'always'
  expands the terms always. 'off' turns off auto-expansion.  Auto-expansion helps
  you to improve the search result e.g. for mis-spelled words. Using auto-expansion
  might slow down the query performance.

- `ranking` - 0|1|True|False enables/disables (default 0|False) relevance ranking
  based on the cosine measure. Using 'ranking' requires that the index uses
  storage(s) that implement IStorageWithTermFrequency
  (txng.storages.term_frequencies). By default an index *does not use* this
  storage (see 'storage' parameter of the index constructor).

- `ranking_maxhits` - the maximum number of documents obtained from the
  ranking (default 50). 'ranking' must be set to True to use this option
  otherwise an exception will be raised.
   

Parsers
=======

TextIndexNG comes with five query parsers. Each of them implements a
different query syntax:

- `txng.parsers.en` - implements the query syntax as described below (this
  is the default query parser)

- `txng.parsers.de` - same as txng.parsers.en but it uses 'UND', 'ODER' and
  'NICHT' instead of 'AND', 'OR' and 'NOT' (german parser)

- `txng.parsers.fr` - same as txng.parsers.en but it uses 'ET', 'OUT' and
  'PAS' instead of 'AND', 'OR' and 'NOT' (french parser)

- `txng.parser.dumb_and` - this is a very simple parser that accepts only a
  whitespace separated list of terms which are all combined using AND. No
  fancy query options as with the parsers above are allowed.

- `txng.parser.dumb_or` - this is a very simple parser that accepts only a
  whitespace separated list of terms which are combined using OR. No fancy
  query options as with the parsers above are allowed.
    


Stemming
========

Wikipedia defines:: 

    A stemmer is a program or algorithm which determines the 
    morphological root of a given inflected (or, sometimes, derived) 
    word form -- generally a written word form.
    

TextIndexNG V3 includes the Snowball stemmer library written by Martin
Porter (snowball.tartarus.org) which provides stemming support for eleven
languages. Stemming is an optional feature and must be specified when you
create a new index. But note that stemming is incompatible by design with a
number of TextIndexNG's features. In general all features except searching for
words without wildcards, left/right truncation  won't work and raise an
exception.


Thesaurus
=========

A thesaurus maps a query term to a sequence of related terms that will be
used for searching. Therefore a thesaurus only affects searching but not
indexing.  Thesaurus are configured as named utitities implementing IThesaurus.
The name of a configured thesaurus is by convention 'txng.thesaurus.XXX' where
XXX is a country code. Multiple thesauruses for one language can be configured
under different names. To tell TextIndexNG3 to use a thesaurus while searching
you must use the name of a thesaurus or a list of thesaurus names as 'thesarus'
parameter to the search() method.

Example::

    index.search(some_query, thesaurus=('txng.thesaurus.de', 'txng.thesaurus.de-special'), ..)

    In this case TextIndexNG will use all query terms from 'some_query' and all related
    terms from a lookup in the configured thesauruses *.de and *.de-special.

Limitation:

Using a thesaurus is not compatible with phrases searches. Terms appearing
within a phrase search will never be used for a thesaurus lookup.


Running the unittests:
======================

    bin/zopectl test -s Products.TextIndexNG3


Query syntax for txng.parsers.en parser
---------------------------------------

- ``AND`` search: `word1 AND word2`

- ``OR`` search: `word1 OR word2`

- ``PHRASE`` search:  `"The Zope Book"`

- ``NOT`` search: `word1 NOT word2`
  (searches for - all documents containing 'word1' but not

- ``Similarity`` search: %word 
  (All words similiar to 'word'. The similarity is measured based on the
  Levenshtein distance of two terms.)

- ``Right truncation``:

  use the '*' operator at the end of a prefix to search for all 
  words that start with this prefix::

  `foo*`   matches 'foo', 'foobar', 'foofoo', etc.

- ``Left truncation``

  use the * operator at the beginning of word to search for all words
  that end with this suffix:

  `*bar` matches 'foobar', 'bar', 'abar', etc.

- ``Wildcard search``

  use '?' or '*' within a term 

- ``Range search``: WORD1..WORD2 
  to search for all words words between WORD1
  and WORD2 where WORD1 <= word <= WORD2 (lexicographical ordering)

- ``Combining queries`` (by example)

  - `word1 and (word2 or word3)`
  - `word1 and (word2 word3)` - a missing operator implies AND search
  - `word1 and "this is a phrase"` search for the phrase AND word1
  - `(word1 or word2) and (word3 or word4)`

- ``multi-field queries``

  Searching over multiple fields is supported using the following
  notation::
    
    `FIELDNAME::OPERATOR(term1 term2 ...)`

  where 'FIELDNAME' is the id of a field as configured for the index.
  'OPERATOR' is either 'phrase', 'near', 'and' or 'not' (or the uppercase
  variant). 'termX' is either a word or a word with a modifier (truncation,
  wildcard search, similarity).

  Examples:

    `title::phrase(The Zope Book)`

    `author::and(michel pelletier amos lattmeier)`

    `title::phrase(The Zope Book) AND author::and(michel pelletier amos lattmeier)`

    `title::phrase(The Zope Book) OR author::and(michel pelletier amos lattmeier)`
    

Query constraints
-----------------

- a word is a sequence of characters that does not contain a whitespace

- all queries must be passed as Python unicode string (not UTF-8 string).
  If a query is not unicode it will be converted to unicode using the 
  configured default encoding.
    
- terms of a phrase (using phrase search) can not contain any special
  operator (for truncation, similiarity search etc)...only whole words

- Left truncation, wildcard search and similarity search are *expensive*
  operations because the index has to iterate over all indexed words
  from the vocabulary to filter out matching words. 



Contact
=======

| ZOPYX Ltd. 
| Hundskapfklinge 33
| D-72074 Tuebingen, Germany
| E-mail: info at zopyx dot com
| Web: http://www.zopyx.com
