function updateStockList(){
    var deferred = $.Deferred();
    $('#basic_setup').addClass('loading');
    $.ajax({
        url: '/admin/update_stock_list',
        type: 'GET'
    }).done(function(){
        $('#basic_setup').removeClass('loading');
        $('#basic_setup_msg_success').removeClass('hidden');
        $('#basic_setup_msg_error').addClass('hidden');
        deferred.resolve();
    }).fail(function(){
        $('#basic_setup').removeClass('loading');
        $('#basic_setup_msg_success').addClass('hidden');
        $('#basic_setup_msg_error').removeClass('hidden');
        deferred.reject();
    });
    return deferred.promise()
}

$(function(){
    $("#update_stock_list").click(function(event) {
        updateStockList();
    });
    $('.message .close').on('click', function() {
        $(this).closest('.message').addClass('hidden');
    });
});