(function($){
    $(document).ready(function(){
        $(document).on("change", ".django-yearmonth-widget-year-selector", function(){
            var year = $(this).val();
            var month = $(this).next().val();
            var day = $(this).prev().attr("data-day-value");
            var value_dumps = $(this).prev().attr("data-value-dumps");
            var value = "";
            if(year && month){
                // value = year + "-" + month + "-" + day;
                value = sprintf(value_dumps, {
                    year: year,
                    month: month,
                    day: day
                });
            }
            $(this).prev().attr("value", value);
        });
        $(document).on("change", ".django-yearmonth-widget-month-selector", function(){
            var year = $(this).prev().val();
            var month = $(this).val();
            var day = $(this).prev().prev().attr("data-day-value");
            var value_dumps = $(this).prev().prev().attr("data-value-dumps");
            var value = "";
            if(year && month){
                // value = year + "-" + month + "-" + day;
                value = sprintf(value_dumps, {
                    year: year,
                    month: month,
                    day: day
                });
            }
            $(this).prev().prev().attr("value", value);
        });
    });
})(jQuery);