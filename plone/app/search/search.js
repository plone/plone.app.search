/* The following line defines global variables defined elsewhere. */
/*globals jQuery, portal_url, Modernizr, alert, history, window, location*/


(function ($) {

    $(function () {

        var container, data, updateResults, pushState;
        container = $('#search-results');

        $('#search-filter input.searchPage[type="submit"]').hide();

        updateResults = function (data) {
            var str, struct, st, initData;
            initData = data;
            $.ajax({
                url: '@@updated_search',
                data: data,
                success: function (data) {
                    container.hide();
                    container.html(data);
                    $(container).fadeIn('medium');

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

        $('form.searchPage').submit(function (e) {
            data = $('form.searchPage').serialize();
            $(container).fadeOut('fast');
            updateResults(data);
            pushState(data);
            e.preventDefault();
        });

        $('#search-filter input, #search-filter select').bind('change', 
            function (e) {
                data = $('form.searchPage').serialize();
                $(container).fadeOut('fast');
                updateResults(data);
                pushState(data);
                e.preventDefault();
            }
        );

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
            updateResults(data);
        });

    });

}(jQuery));
