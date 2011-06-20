/* The following line defines global variables defined elsewhere. */
/*globals jQuery, portal_url, Modernizr, alert, history, window,
location, document*/


(function ($) {

    $(function () {

        var container, data, i, updateResults, pushState;
        container = $('#search-results');

        // We hide the 'Search' button in the filter in order to not confuse
        // the end users with JS enabled. The button is still in HTML for the
        // accessibility reasons for those with JS disabled browsers
        $('#search-filter input.searchPage[type="submit"]').hide();

        updateResults = function (data) {
            var results, current_sorting, new_sorting, unwrapped;
            $.ajax({
                url: '@@updated_search',
                data: data,
                dataType: 'json',
                success: function (data) {
                    // Update the Search term
                    $('#search-term').text(data.search_term);

                    // Update the number of the search results
                    $('#search-results-number').text(data.results_number);

                    // Remove link from the clicked sorting option and wrap
                    // the previous sorting into an <a/>:
                    current_sorting = $('#sorting-options strong');
                    for (i = 0; i < data.search_options.length; i += 1) {
                        if (data.search_options[i].selected) {
                            new_sorting = $('#sorting-options').children().filter('strong, a')[i];
                            $(new_sorting).wrapInner('<strong />');
                            $(new_sorting).children('strong').unwrap();
                        }
                        if (data.search_options[i].title === $(current_sorting).text()) {
                            current_sorting.wrapInner('<a />');
                            unwrapped = current_sorting.children('a').unwrap();
                            unwrapped.attr('href', data.search_options[i].url);
                            unwrapped.attr('data-sort', data.search_options[i].sortkey);
                        }
                    }

                    // Get the updated results. Attributes are based on what
                    // we are getting from IContentListingObject, since this is
                    // the main wrapper around the listings in Plone 4.2+.
                    // Check that interface to figure out what other information
                    // can be got for any particular listing item — we are
                    // getting all methods except getObject()

                    // We don't simply hide() the container, but change it's
                    // opacity in order for the container keep it's place in the
                    // elements' flow while we make AJAX call and are getting the
                    // updated results. This gives us smoother transition from
                    // one results to another.
                    container.hide();

                    results = function () {
                        var dl_elem, template;

                        // We initialize the wrapping DL element that holds
                        // all the search results
                        dl_elem = document.createElement('dl');
                        dl_elem.setAttribute('class', 'searchResults');

                        for (i = 0; i < data.results.length; i += 1) {
                            // var link_elem = document.createElement('a');
                            // link_elem.setAttribute('href', data.results[i].getURL);
                            // link_elem.setAttribute('class', 'state-' + data.results[i].review_state);
                            // link_elem.innerHTML = data.results[i].Title;
                            // 
                            // var dt_elem = document.createElement('dt');
                            // dt_elem.setAttribute('class', 'contenttype-' + data.results[i].Type.toLowerCase());
                            // $(dt_elem).html(link_elem);

                            // var div_elem = document.createElement('div');
                            // div_elem.innerHTML = data.results[i].CroppedDescription;

                            template = '<dt class="contenttype-%portal_type%">' +
                                       '    <a class="state-%workflow_state%" href="%item_url%">%Title%</a>' +
                                       '</dt>' +
                                       '<dd>' +
                                       '     <div>%Description%</div>' +
                                       '</dd>';

                            template = template.replace('%portal_type%', data.results[i].Type.toLowerCase());
                            template = template.replace('%workflow_state%', data.results[i].review_state);
                            template = template.replace('%item_url%', data.results[i].getURL);
                            template = template.replace('%Title%', data.results[i].Title);
                            template = template.replace('%Description%', data.results[i].Description);

                            $(dl_elem).append(template);
                        }

                        return dl_elem;
                    };

                    container.html(results());
                    container.fadeIn();

                    // Update RSS link
                    $('#rss-subscription a.link-feed').attr('href', function () {
                        return portal_url + '/search_rss?SearchableText=' + data.search_term;
                    });
                },
                error: function (req, error) {
                    return true;
                }
            });
        };

        pushState = function (initData) {
            // Now we need to update the browser's path bar to reflect
            // the URL we are at now and to push a history state change
            // in the browser's history. We are using Modernizr
            // library to check whether browser supports HTML5 History
            // API natively or it needs a polyfill, that provides
            // hash-change events to the older browser
            if (Modernizr.history) {
                // portal_url is the global JS variable available
                // everywhere in Plone
                var url = portal_url + '/@@search?' + initData;
                history.pushState(null, null, url);
            }
        };

        // We don't submit the whole form with all the fields when only the
        // search term is being changed. We just alter the current URL to
        // substitue the search term and make a new ajax call to get updated
        // results
        $('#searchPage input.searchPage').click(function (e) {
            var st, query;
            st = $('#search-field input.searchPage').val();
            query = location.search.replace(/SearchableText=[^&]*/, 'SearchableText=' + st);
            data = query.split('?')[1];
            $(container).fadeOut('fast');
            updateResults(data);
            pushState(data);
            e.preventDefault();
        });
        $('form.searchPage').submit(function (e) {
            data = $('form.searchPage').serialize();
            $(container).fadeOut('fast');
            updateResults(data);
            pushState(data);
            e.preventDefault();
        });

        // We need to update the site-wide search field (at the top right in
        // stock Plone) when the main search field is updated
        $('#search-field input[name="SearchableText"]').keyup(function () {
            $('input#searchGadget').val($(this).val());
        });


        // When we click any option in the Filter menu, we need to prevent the
        // menu from being closed as it is dictaded by dropdown.js for all
        // dl.actionMenu > dd.actionMenuContent
        $("#search-results-bar dl.actionMenu > dd.actionMenuContent").click(function (e) {
            e.stopImmediatePropagation();
        });

        // Now we can handle the actual menu options and update the search
        // results after any of them has been chosen.
        $('#search-filter input, #search-filter select').bind('change', 
            function (e) {
                data = $('form.searchPage').serialize();
                $(container).fadeOut('fast');
                updateResults(data);
                pushState(data);
                e.preventDefault();
            }
        );

        // Since we replace the whole sorting options with HTML, coming in
        // AJAX response, we should bind the click event with live() in order
        // for this to keep working with the HTML elements, coming from AJAX
        // respons
        $('#sorting-options a').live('click', function (e) {
            if ($(this).attr('data-sort')) {
                $("form.searchPage input[name='sort_on']").val($(this).attr('data-sort'));
            }
            else {
                $("form.searchPage input[name='sort_on']").val('');
            }
            data = this.search.split('?')[1];
            updateResults(data);
            pushState(data);
            e.preventDefault();
        });

        // No need to wrap 'popstate' event handler for window object with
        // Modernizr check up since popstate event will contain any data only if
        // a state has been created with history.pushState() that is wrapped in
        // Modernizr checkup above
        $(window).bind('popstate', function () {
            data = location.search.split('?')[1];
            // We need to make sure we update the search field with the search
            // term from previous query when going back in history
            var str = data.match(/SearchableText=[^&]*/)[0];
            str = str.replace(/\+/g, ' '); // we remove '+' used between words 
            // in search queries.

            // Now we have something like 'SearchableText=test' in str
            // variable. So, we know when the actual search term begins at
            // position 15 in that string.
            $('#search-field input[name="SearchableText"], input#searchGadget').val(str.substr(15, str.length));

            updateResults(data);
        });

    });

}(jQuery));
