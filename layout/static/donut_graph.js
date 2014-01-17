var getStatistics = function(daysFromNow, onSuccess){
    var now, dateFrom, dateTo;
    $('.js-activity-chart').data('currentDays', daysFromNow);
    now = new Date();
    dateTo = moment(now).format('YYYY-MM-DDTHH:m:s');
    dateFrom = moment(new Date(now - daysFromNow * 24 * 60 * 60 * 1000)).format('YYYY-MM-DDTHH:m:s');
    $.ajax(
        '/api/profile/statistics?date_from=' + dateFrom + '&date_to=' + dateTo
    ).success(function(data){
        console.log(daysFromNow, dateFrom, dateTo, data);
        onSuccess(data);
    });

};
var drawDonutGraph = function(graphData){
    var ctx = $(".js-activity-chart").get(0).getContext("2d"),
            data = [];
    $.each(graphData, function(key, value){
        data.push({
            value: value['relative_value'],
            color: value['color']
        })
    });
    new Chart(ctx).Doughnut(data, {});
};
