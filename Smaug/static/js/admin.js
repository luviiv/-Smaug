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

function updateFinanceSummary(){
    var deferred = $.Deferred();
    $.ajax({
        url: '/admin/update_finance_summary',
        type: 'GET'
    })
    .done(function() {
        deferred.resolve();
    })
    .fail(function() {
        deferred.reject();
    });
    return deferred.promise();
}

$(function(){
    $("#update_stock_list").click(function(event) {
        updateStockList();
    });
    $("#update_finance_summary").click(function(event) {
        updateFinanceSummary();
    });
    $('.message .close').on('click', function() {
        $(this).closest('.message').addClass('hidden');
    });
});