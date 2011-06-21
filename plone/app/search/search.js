/* The following line defines global variables defined elsewhere. */
/*globals jQuery, portal_url, Modernizr, alert, history, window, location*/


(function ($) {

    $(function () {

        var container, data, updateResults, pushState, popped, initialURL;
        container = $('#search-results');

        $('#search-filter input.searchPage[type="submit"]').hide();

        updateResults = function (data) {
            var str, struct, st;
            $.ajax({
                url: '@@updated_search',
                data: data,
                success: function (data) {
                    // We don't simply hide() the container, but change it's
                    // opacity in order for the container keep it's place in the
                    // elements' flow while we make AJAX call and are getting the
                    // updated results. This gives us smoother transition from
                    // one results to another.
                    container.hide();
                    container.html(data);
                    container.fadeIn();

                    st = $('#updated-search-term').text();
                    if ($('#search-term').length === 0) {
                        // Until now we had queries with empty search term. So
                        // we need a placeholder for the search term in
                        // result's title.
                        $('h1.documentFirstHeading').append('<strong id="search-term" />');
                    }
                    $('#search-term').text(function () {
                        str = st;
                        $('#updated-search-term').remove();
                        return str;
                    });

                    $('#search-results-number').text(function () {
                        str = $('#updated-search-results-number').text();
                        $('#updated-search-results-number').remove();
                        return str;
                    });
                    $('#search-results-bar #sorting-options').html(
                        function () {
                            struct = $('#updated-sorting-options').html();
                            $('#updated-sorting-options').remove();
                            return struct;
                        }
                    );
                    $('#rss-subscription a.link-feed').attr('href', function () {
                        return portal_url + '/search_rss?SearchableText=' + st;
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
        $('#search-results-bar dl.actionMenu > dd.actionMenuContent').click(function (e) {
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

        // THE HANDLER FOR 'POPSTATE' EVENT IS COPIED FROM PJAX.JS
        // https://github.com/defunkt/jquery-pjax

        // Used to detect initial (useless) popstate.
        // If history.state exists, assume browser isn't going to fire initial popstate.
        popped = ('state' in window.history);
        initialURL = location.href;


        // popstate handler takes care of the back and forward buttons
        //
        // No need to wrap 'popstate' event handler for window object with
        // Modernizr check up since popstate event will contain any data only if
        // a state has been created with history.pushState() that is wrapped in
        // Modernizr checkup above.
        $(window).bind('popstate', function (event) {
            var initialPop, str;
            // Ignore inital popstate that some browsers fire on page load
            initialPop = !popped && location.href === initialURL;
            popped = true;
            if (initialPop) {
                return;
            }

            data = location.search.split('?')[1];
            // We need to make sure we update the search field with the search
            // term from previous query when going back in history
            str = data.match(/SearchableText=[^&]*/)[0];
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
