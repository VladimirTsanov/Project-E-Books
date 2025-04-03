$(document).ready(function(){ 
    $(".filter-checkbox").on('click', function(){
        var _filterObj = {};

        $(".filter-checkbox:checked").each(function(){
            var _filterKey = $(this).closest('li').data('filter');
            var _filterVal = $(this).closest('li').clone().children().remove().end().text().trim();

            if (!_filterKey) {
                console.warn("data-filter липсва в <li>", $(this).closest('li'));
                return;
            }

            if (!_filterObj[_filterKey]) {
                _filterObj[_filterKey] = [];
            }
            _filterObj[_filterKey].push(_filterVal);
        });

        //Run Ajax
        $.ajax({
            url:'/filter-data',
            data: _filterObj,
            dataType: 'json',
            beforeSend: function(){
                $("#filteredProducts").html('Loading ...');

            },
            success:function(res){
                console.log(res);
                
            }
        });
    });
});
