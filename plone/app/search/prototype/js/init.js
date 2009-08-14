$(function(){
    $('.actionMenuHeader').click(function() {
        $(this).parent().children("dd").toggle();
        return false;
    });
    $('#cancel').click(function() {
        $(this).parents('.actionMenuContent').hide();
    });
    $('#save').click(function() {
        $('.portalMessage dd').html('Collection is saved at: <a href="#">/Folder1/</a>');
        $('.portalMessage').show();
        $(this).parents('.actionMenuContent').hide();
    });
    $('#advancedsearchlink').click(function() {
        $('#simplesearch').hide();
        $('#advancedsearch').show();
        return false;
    });
});
