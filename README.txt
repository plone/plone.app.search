Introduction
============

This package implements alternative group-based search behaviours for Plone
3.1. Group based searches group search results in reasonably broad groups,
which gives users a fast way to narrow searches down to the type of thing
they are interested at. This package aims to implement two types of
grouping: groups based on categories (where a category is just a subset of
the site) and groups based on portal types (for example 'downloads' and
'documents').

There is no alternative provided for the advanced search feature as included
with stock Plone: this is better handled through a filter/facet-based
approach.



Category based search
---------------------

After installing this package all folders in the site can be marked as a
'category'. You can do this when editing a folder via a new option in the
*edit* tab.

All site searches, both normal search and live-search, will show the first
five results for each category. To get more search results for a specific
category just click on its title.

In addition when you are in a category you can select to only search within
that category through a toggle next to the search box.


Still to do
-----------

* Search using type groups (downloads / documents / etc.)

* determine how to handle the navigation root. Should we only show categories
  under the current navigation root? I suspect it will fairly common to use
  a category as a navigation root so this seem undesirable.

