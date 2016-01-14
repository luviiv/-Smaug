function MyStocks(){
    var self = this;
    var baseUrl = "/dynamic_data?list=";
    this.loadGrid = function(){
        var stockList = getMyStockList();
        var queryUrl = baseUrl;
        for(idx in stockList){
            queryUrl=queryUrl+(idx==0?"":",");
            if(stockList[idx].substring(0,1)=="6"){
                queryUrl=queryUrl+"sh"+stockList[idx];
            }else{
                queryUrl=queryUrl+"sz"+stockList[idx];
            }
        }
        refreshGrid(queryUrl);
    };
    function refreshGrid(_queryUrl){
        $.ajax({
            url: _queryUrl,
            type: 'GET',
            success: function(response){
                var results = response.split('\n');
                var mappedResults = {};
                for(var i=0;i<results.length-1;i++){
                    var code = results[i].substring(13,19);
                    var values = results[i].substring(21, results[i].length-2).split(",");
                    mappedResults[code] = values;
                }
                $('#my-stocks tbody tr').each(function(index, el) {
                    var code = $(this).find('td[data-field="code"]').text().trim();
                    values = mappedResults[code];
                    $(this).find('td[data-field="name"]').text(values[0]);
                    $(this).find('td[data-field="today-open"]').text(parseFloat(values[1]).toFixed(2));
                    $(this).find('td[data-field="yesterday-close"]').text(parseFloat(values[2]).toFixed(2));
                    $(this).find('td[data-field="new-price"]').text(parseFloat(values[3]).toFixed(2));
                    $(this).find('td[data-field="highest"]').text(parseFloat(values[4]).toFixed(2));
                    $(this).find('td[data-field="lowest"]').text(parseFloat(values[5]).toFixed(2));
                    $(this).find('td[data-field="buy"]').text(parseFloat(values[6]).toFixed(2));
                    $(this).find('td[data-field="sell"]').text(parseFloat(values[7]).toFixed(2));
                    $(this).find('td[data-field="amount"]').text((values[8]/100).toFixed(0));
                    $(this).find('td[data-field="turnover"]').text((values[9]/10000).toFixed(2));
                    $(this).find('td[data-field="price-change"]').text(formatSignedNumber(values[3]-values[2]));
                    $(this).find('td[data-field="price-limit"]').text(formatSignedNumber((values[3]-values[2])/values[2]*100)+'%');
                });
            }
        });
        
        function formatSignedNumber(_v){
            if(_v<0){
                return '-'+Math.abs(_v).toFixed(2);
            }else if(_v>0){
                return '+'+Math.abs(_v).toFixed(2);
            }else{
                return parseFloat(_v).toFixed(2);
            }
        }
    }
    function getMyStockList(){
        var mystocks = [];
        $('#my-stocks tbody tr').each(function(index, el) {
            var code = $(this).find('td[data-field="code"]').text().trim();
            mystocks.push(code);
        });
        return mystocks;
    }
};

$(function(){
    var mystocks = new MyStocks();
    mystocks.loadGrid();
});