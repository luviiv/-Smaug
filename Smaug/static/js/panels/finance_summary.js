function SummaryGrid(){
    var self = this;

    var DECEMBER = /-12-/;
    var MARCH = /-03-/;
    var JUNE = /-06-/;
    var SEPTEMBER = /-09-/;
    //regexp to test if matches the month
    this.loadGrid = function(){
        var queryUrl = $('#query_url').val();
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
            width: 900,
            height: 460,
            loadComplete: function(){
                enableFilterButtons();
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

    this.bindActions = function(){
        $('#all').click(function(event) {
            self.filterByDeadLine("all");
        });
        $('#march').click(function(event) {
            self.filterByDeadLine(MARCH);
        });
        $('#june').click(function(event) {
            self.filterByDeadLine(JUNE);
        });
        $('#september').click(function(event) {
            self.filterByDeadLine(SEPTEMBER);
        });
        $('#december').click(function(event) {
            self.filterByDeadLine(DECEMBER);
        });
        $('#search_stock').change(searchStock);
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
        alert("yes");
    }
}

$(function(){
    var summaryGrid = new SummaryGrid();
    summaryGrid.bindActions();
    summaryGrid.loadGrid();
});
