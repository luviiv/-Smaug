function SummaryGrid(){
    this.loadGrid = function(_code){
        var queryUrl = $('#query_url').val();
        $("#summary_grid").jqGrid({
            url: queryUrl,
            mtype: "GET",
            datatype: "json",
            colModel: [
                {label: $('#dead_line').val(), name: 'dead_line', key: true, fixed: true, width: 75, frozen: true, sortable: false},
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
            height: 460
        });
        
        $("#summary_grid").jqGrid("setFrozenColumns");
    }
}

$(function(){
    var summaryGrid = new SummaryGrid();
    summaryGrid.loadGrid('600000');
});
