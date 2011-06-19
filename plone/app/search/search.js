/* The following line defines global variables defined elsewhere. */
/*globals jQuery, portal_url, Modernizr, alert, history, window, location*/


(function ($) {

    $(function () {

        var container, data, updateResults, pushState;
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

        $(window).bind('popstate', function () {
            data = location.search.split('?')[1];
            // var st = data.replace(/^.+SearchableText=(.*).*$/, '$1');
            updateResults(data);
        });

    });

}(jQuery));
