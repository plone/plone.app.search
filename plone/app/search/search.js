/* The following line defines gliobal variables defined elsewhere. */
/*global jQuery:false*/

(function ($) {

    $(function () {

        var container, data;
        container = $('#search-results');

        function updateResults(data) {
            var str, struct;
            $.ajax({
                url: '@@updated_search',
                data: data,
                success: function (data) {
                    container.hide();
                    container.html(data);
                    $(container).fadeIn('medium');
                    $('#search-results-number').text(function () {
                        str = $('#updated-search-results-number').text();
                        $('#updated-search-results-number').remove();
                        return str;
                    });
                    $('#searchResultsHeading #sorting-options').html(
                        function () {
                            struct = $('#updated-sorting-options').html();
                            $('#updated-sorting-options').remove();
                            return struct;
                        }
                    );
                },
                error: function (req, error) {
                    return true;
                }
            });
        }

        $('form.searchPage').submit(function () {
            data = $('form.searchPage').serialize();
            $(container).fadeOut('fast');
            updateResults(data);
            return false;
        });

        $('#search-filter input, #search-filter select').bind('change', 
            function () {
                data = $('form.searchPage').serialize();
                $(container).fadeOut('fast');
                updateResults(data);
                return false;
            }
        );

        $('#sorting-options a').live('click', function () {
            if ($(this).attr('rel')) {
                $("form.searchPage input[name='sort_on']").val($(this).attr('rel'));
            }
            else {
                $("form.searchPage input[name='sort_on']").val('');
            }
            data = $('form.searchPage').serialize();
            updateResults(data);
            return false;
        });

        $('#show-search-options').click(function () {
            $('#search-results-wrapper').css({'width': '97.75%', 
                                              'margin-left': '-98.875%'});
            $('#search-results-wrapper').removeClass('width-16');
            $('#search-results-wrapper').removeClass('position-0');
            $('#search-filter').hide();
            $('#search-filter').removeClass('hiddenStructure');

            $('#search-results-wrapper').animate({
                width: '72.75%',
                marginLeft: '-73.875%'
            }, 500, function () {
                $('#search-filter').fadeIn('medium');
                $('#show-search-options').delay(500).fadeOut();
            });
            $('#search-results-wrapper').addClass('position-1:4');
            $('#search-results-wrapper').addClass('width-12');
            return false;
        });

        $('#close-search-options').click(function () {
            $('#search-results-wrapper').removeClass('width-12');
            $('#search-results-wrapper').removeClass('position-1:4');
            $('#search-filter').fadeOut('fast', function () {
                $('#search-filter').addClass('hiddenStructure');
                $('#search-results-wrapper').animate({
                    width: '97.75%',
                    marginLeft: '-98.875%'
                }, 500, function () {
                    $('#show-search-options').delay(300).fadeIn();
                });
            });
            $('#search-results-wrapper').addClass('position-0');
            $('#search-results-wrapper').addClass('width-16');
            return false;
        });
    });
}(jQuery));
