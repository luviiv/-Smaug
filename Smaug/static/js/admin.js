function updateStockList(){
    var deferred = $.Deferred();
    $("#close-modal").addClass('smg-hide');
    prepareProgress(false);
    $('#progress').openModal();
    $.ajax({
        url: '/admin/update_stock_list',
        type: 'GET'
    }).done(function() {
        showMsg($("#success-title").val(),$("#success-msg").val());
        deferred.resolve();
    })
    .fail(function() {
        showMsg($("#fail-title").val(),$("#fail-msg").val());
        deferred.reject();
    });
    return deferred.promise()
}

function updateFinanceSummary(){
    var deferred = $.Deferred();
    $("#close-modal").addClass('smg-hide');
    prepareProgress(false);
    $('#progress').openModal();
    $.ajax({
        url: '/admin/update_finance_summary',
        type: 'GET'
    })
    .done(function() {
        showMsg($("#success-title").val(),$("#success-msg").val());
        deferred.resolve();
    })
    .fail(function() {
        showMsg($("#fail-title").val(),$("#fail-msg").val());
        deferred.reject();
    });
    return deferred.promise();
}

function showMsg(_title, _content){
    $("#msg-title").text(_title);
    $("#msg-content").text(_content);
    $("#close-modal").removeClass('smg-hide');
    prepareProgress(true);
}

function prepareProgress(_isend){
    if(_isend){
        $("#progress-bar").removeClass("indeterminate");
        $("#progress-bar").addClass("determinate");
    }else{
        $("#progress-bar").removeClass("determinate");
        $("#progress-bar").addClass("indeterminate");
        $("#msg-title").text($("#msg-t").val());
        $("#msg-content").text($("#msg-c").val());
    }
}

$(function(){
    $("#update_stock_list").click(function(event) {
        updateStockList();
    });
    $("#update_finance_summary").click(function(event) {
        updateFinanceSummary();
    });
    $("#close-modal").click(function(event) {
        $('#progress').closeModal();
    });
});