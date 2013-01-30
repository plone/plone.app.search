Changelog
=========

1.1.2 (2013-01-30)
------------------

- Fix to make search.js work with jQuery >=1.8.
  [garbas]


1.1.1 (2013-01-01)
------------------

- Fixed translation problem with the @@updated_search responses.
  [dokai]

- fix search results when having done a seach and switching out some
  items and doing the same search again, refs #12880
  [maartenkling, robgietema]

- only fill query when there is at least one type selected
  [maartenkling]

- Fixed Google Chrome and Safari search compatibility problem
  https://dev.plone.org/ticket/13249
  [Manabu TERADA]


1.1.0 (2012-10-16)
------------------

- Fix attribute error when portal_syndication can not be found.
  [maurits]


1.0.6 (2012-10-11)
------------------

- JavaScript now correctly obeys navigation root for searches, obtained via
  meta tag set in search.pt.
  [seanupton]


1.0.5 (2012-08-30)
------------------

- Search.filter_query() checks for any valid indexes specified in request
  to prevent empty catalog searches, instead of limiting searches to
  require either SearchableText or Subject query.  This is more permissive,
  but accomplishes the same goal with better generality (possibly allowing
  various cases including the calendar portlet using to @@search, instead
  of deprecated search.pt in Products.CMFPlone).
  [seanupton]

- Define navigation_root_url in search.pt when used in search-results
  macro.
  [seanupton]


1.0.4 (2012-08-23)
------------------

- Fixed regression when using search_results macro from outside template.
  [thomasdesvenain]

- Don't assume that SearchableText is going to be in any url with a GET
  request.
  [eleddy]


1.0.3 (2012-08-11)
------------------

- Check if type uses view action in listing in search results.
  [thomasdesvenain]

- Change breadcrumb separator to / (slash character) for accessibility, and added SEO benefits.
  see https://dev.plone.org/ticket/12904
  [polyester]

- Use convenience class ``width-full`` instead of grid class ``width-16`` in
  search.pt, see https://dev.plone.org/ticket/13054
  [saily]


1.0.2 (2012-02-07)
------------------

- Fix @@search if the parameter SearchableText is missing in the URL.
- Adapt selenium tests for more recent selenium versions.
  [gaudenz]


1.0.1 (2011-10-17)
------------------

- Fix @@search view to return results when we are only looking for a Subject.
  Refs http://dev.plone.org/plone/ticket/12232
  [ggozad]

- Translations moved to plone.app.locales.
  [vincentfretin]


1.0 (2011-07-19)
----------------

- Restrict AJAX handling of the batch navigation links to the search results
  page only and prevent it influencing all of the batch navigations in the
  site.
  [spliter]

- Re-structuring the JS actions, happening after successful call to
  @@updated_search to make the animations smoother.
  [spliter]

- Labels for the 'New items since' section of the 'Filter the results'
  dropdown are actual labels now.
  References http://dev.plone.org/plone/ticket/12005
  [spliter]

- Don't make the search view available only on folderish items, since the
  context is not used within the view and it needs to be available for
  plone.app.collection.
  [davisagli]

- Handle a portal_type criterion specified as a dictionary.
  [davisagli]

- Don't abort the query entirely in filter_query if no SearchableText was
  specified.
  [davisagli]

- Re-add unbatched option to the search results method (it is used by
  plone.app.collection).
  [davisagli]

- RSS link is being updated after changing search term and updating the
  results with ajax call.
  [spliter]

- Search term is updated after ajax calls
  [spliter]

- Add MANIFEST.in.
  [WouterVH]

- Added plone.app.contentlisting as a dependency for the package.
  [spliter]

- Added title and description to the GS profile.
  [spliter]

- Moved search.js from CMFPlone into the package.
  [spliter]

- Fixed catalog query to treat 'use_types_blacklist' parameter properly so that
  types excluded from search at @@search-controlpanel would not show up in the
  search results page.
  [spliter]

- Fixed the issue with 'relevance' sorting option when it was not highlighted
  as the current one after getting back to it after some ajax calls.
  [spliter]

- Moved performance and selenium tests to dedicated tests folders in order to
  exclude those from the general testing.
  [spliter]

- Fixed a bug that prevented @@search to work for authenticated members.
  [zupo]

- Selenium test for standard @@search view without interactions.
  [spliter]

- Base for Selenium tests and basic test.
  [zupo]

- 'Close' button for advanced search filter column
  [spliter]

- Moved the duplicate of the search button in search form to the
  bottom of the "filter" column in order to have better accessibility
  when JS is disabled.
  Referencese http://dev.plone.org/plone/ticket/9352
  [spliter]

- Ajax calls to update search results on the fly.
  Referencese http://dev.plone.org/plone/ticket/9352
  [spliter]

- Replaced url in search results with a Location -> it displays
  the search results item's first-level folder aka. a section.
  For first-level items, nothing is displayed.
  [zupo]

- New view for the fetching search results on the fly.
  Referencese http://dev.plone.org/plone/ticket/9352
  [spliter, witsch]

- Advanced search form a.k.a. Search filter is being merged into
  search result with JS hide/show.
  [spliter]

- Added truncating the search result's location url, in case it's too
  long.
  [zupo]

- Added condition to only display modification date if it is
  different than publication date.
  [zupo]

- Merge the advanced and basic searches into one.
  [dukebody]

- Added publication date to a search result.
  [zupo]

- Styling the author and modification date of a search result to
  look like it was proposed in PLIP #9352.
  [zupo]

- Add RSS icon to the search feed results and clarify associated text.
  [dukebody]

- Display a short modification date using toLocalizedTime with
  long_format parameter set to false.
  [zupo]

- Hide documentbyline when user is anonymous and the allow anonymous
  view about setting is set to false.
  [robgietema]

- Fixed author url.
  [robgietema]

- Show username when fullname is not specified.
  [robgietema]

- Fixed template layout.
  [robgietema]

- Removed querybuilder and unused views.
  [robgietema]

- Initial checkin.
  [elvix]
