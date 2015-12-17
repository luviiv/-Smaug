function SummaryGrid(){
    var self = this;

    var DECEMBER = /-12-/;
    var MARCH = /-03-/;
    var JUNE = /-06-/;
    var SEPTEMBER = /-09-/;
    var ALL = 'all';
    var currentMonth = ALL;
    var currentParam = 'main_business_revenue';

    var no_result = $('#search_result').text();
    var current_stock = {}
    current_stock.code = $('#title_code').text();
    current_stock.name = $('#title_name').text();

    var million_param = ['main_business_revenue',
                        'net_profit',
                        'total_long_term_liabilities',
                        'financial_expenses',
                        'total_current_assets',
                        'total_assets',
                        'total_fixed_assets'];
    //regexp to test if matches the month
    this.loadGrid = function(_code){
        var queryUrl = '/finance_summary/'+_code;
        $("#summary_grid").jqGrid({
            url: queryUrl,
            mtype: "GET",
            datatype: "json",
            colModel: [
                { label: $('#dead_line').val(), name: 'dead_line', key: true, fixed: true, width: 75, frozen: true, sortable: false},
                { label: $('#main_business_revenue').val(), name: 'main_business_revenue', fixed: true, frozen: true, sortable: false },
                { label: $('#net_profit').val(), name: 'net_profit', fixed: true, frozen: true, width: 75, sortable: false },
                { label: $('#total_long_term_liabilities').val(), name: 'total_long_term_liabilities', fixed: true, frozen: true, sortable: false },
                { label: $('#net_assets_value_per_share').val(), name: 'net_assets_value_per_share', fixed: true, frozen: true, sortable: false },
                { label: $('#earnings_per_share').val(), name: 'earnings_per_share', fixed: true, sortable: false},
                

                { label: $('#cash_flow_per_share').val(), name: 'cash_flow_per_share', fixed: true, sortable: false },
                { label: $('#financial_expenses').val(), name: 'financial_expenses', fixed: true , sortable: false},
                { label: $('#total_current_assets').val(), name: 'total_current_assets', fixed: true , sortable: false},
                { label: $('#total_fixed_assets').val(), name: 'total_fixed_assets', fixed: true , sortable: false},
                { label: $('#total_assets').val(), name: 'total_assets', fixed: true , sortable: false}
                
            ],
            viewrecords: true,
            rowNum: -1,
            width: 900,
            height: 460,
            loadComplete: function(){
                enableFilterButtons();
                self.loadTrendTable();
            }
        });
        
        $("#summary_grid").jqGrid("setFrozenColumns");
    };

    this.filterByDeadLine = function(_month){
        var rows = $('#summary_grid tr');
        for(var i=1;i<rows.length;i++){
            if(_month=="all"){
                $('#summary_grid tr[id="'+rows[i].id+'"]').removeClass('smg-hide');
                $('#summary_grid_frozen tr[id="'+rows[i].id+'"]').removeClass('smg-hide');
            }else if(_month.test(rows[i].id)){
                $('#summary_grid tr[id="'+rows[i].id+'"]').removeClass('smg-hide');
                $('#summary_grid_frozen tr[id="'+rows[i].id+'"]').removeClass('smg-hide');
            }else{
                $('#summary_grid tr[id="'+rows[i].id+'"]').addClass('smg-hide');
                $('#summary_grid_frozen tr[id="'+rows[i].id+'"]').addClass('smg-hide');
            }
        }
    };

    this.loadTrendTable = function(){
        var _month = currentMonth;
        var _columnName = currentParam;
        var seasonData = [];
        var seasonDeadLine = [];
        var allData = [];
        var allDeadLine = [];
        var summaries = $('#summary_grid').jqGrid('getCol',_columnName, true);

        var unit = '';
        if($.inArray(currentParam, million_param)!=-1){
            unit = $('#million').val();
        }
        //filter rows by month
        for(var i=summaries.length-1;i>=0;i--){
            var data = unit==''?summaries[i].value:(summaries[i].value/100);
            if(_month==ALL){
                seasonData.push(data);
                seasonDeadLine.push(summaries[i].id);
            }else if(_month.test(summaries[i].id)){
                seasonData.push(data);
                seasonDeadLine.push(summaries[i].id);
            }
        }
        
        var lineLabel = $('#all').text();
        if(_month==MARCH){
            lineLabel = $('#march').text();
        }else if(_month==JUNE){
            lineLabel = $('#june').text();
        }else if(_month==SEPTEMBER){
            lineLabel = $('#september').text();
        }else if(_month==DECEMBER){
            lineLabel = $('#december').text();
        }
        //setup trend table
        require.config({
            paths: {
                echarts: 'http://echarts.baidu.com/build/dist'
            }
        });
        require(
            [
                'echarts',
                'echarts/chart/line'
            ],function (ec) {
                var myChart = ec.init(document.getElementById('trend-table')); 
                var option = {
                    title : {
                        text: $('#'+currentParam).val(),
                        subtext: unit
                    },
                    tooltip : {
                        trigger: 'axis'
                    },
                    legend: {
                        data:[lineLabel]
                    },
                    toolbox: {
                        show : true,
                        feature : {
                            mark : {show: true},
                            dataView : {show: true, readOnly: false},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    calculable : true,
                    xAxis : [
                        {
                            type : 'category',
                            boundaryGap : false,
                            data : seasonDeadLine
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value'
                        }
                    ],
                    series : [
                        {
                            name:lineLabel,
                            type:'line',
                            stack: '总量',
                            data:seasonData
                        }
                    ]
                };
                myChart.setOption(option); 
            }); 
    };

    this.bindActions = function(){
        $('#all').click(function(event) {
            currentMonth = ALL;
            self.filterByDeadLine("all");
            self.loadTrendTable();
        });
        $('#march').click(function(event) {
            currentMonth = MARCH;
            self.filterByDeadLine(MARCH);
            self.loadTrendTable();
        });
        $('#june').click(function(event) {
            currentMonth = JUNE;
            self.filterByDeadLine(JUNE);
            self.loadTrendTable();
        });
        $('#september').click(function(event) {
            currentMonth = SEPTEMBER;
            self.filterByDeadLine(SEPTEMBER);
            self.loadTrendTable();
        });
        $('#december').click(function(event) {
            currentMonth = DECEMBER;
            self.filterByDeadLine(DECEMBER);
            self.loadTrendTable();
        });
        $('#trend-column').change(function(){
            currentParam = $('#trend-column').val();
            self.loadTrendTable();
        });
        $('#search_stock').change(searchStock);
        $('#search_result').blur(function(event) {
            $('#search_result').addClass('smg-hide');
        });
        $('#search_result').click(function(event) {
            $('#search_result').addClass('smg-hide');
            disableFilterButtons();
            if(self.current_stock!=null){
                $('#title_code').text(self.current_stock.code);
                $('#title_name').text(self.current_stock.name);
                $("#summary_grid").jqGrid('GridUnload');
                self.loadGrid(self.current_stock.code);
                $('#title_code').parent().animate({
                    color: "red"
                }, 2000 );
                setTimeout(function(){
                    $('#title_code').parent().animate({
                        color: "black"
                    }, 2000 );
                }, 6000);
            }
        });
    };

    function enableFilterButtons(){
        $('#all').removeAttr("disabled");
        $('#march').removeAttr("disabled");
        $('#june').removeAttr("disabled");
        $('#september').removeAttr("disabled");
        $('#december').removeAttr("disabled");
    }
    function disableFilterButtons(){
        $('#all').attr("disabled","true");
        $('#march').attr("disabled","true");
        $('#june').attr("disabled","true");
        $('#september').attr("disabled","true");
        $('#december').attr("disabled","true");
    }

    function searchStock(){
        $.ajax({
            url: '/fetchdata/querystock/'+$('#search_stock').val(),
            type: 'GET'
        }).then(function(back){
            if(back.stock==null){
                $('#search_result').text(no_result);
                $('#search_result').removeClass('blue')
                $('#search_result').addClass('red');
                self.current_stock = null;
            }else{
                $('#search_result').text(back.stock.code+' '+back.stock.name);
                $('#search_result').removeClass('red')
                $('#search_result').addClass('blue');
                self.current_stock = back.stock;
            }
            $('#search_result').removeClass('smg-hide');
            $('#search_result').focus();
        });
    }
}

$(function(){
    var summaryGrid = new SummaryGrid();
    summaryGrid.bindActions();
    summaryGrid.loadGrid($('#title_code').text());
});
