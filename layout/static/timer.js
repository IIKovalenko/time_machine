var interval_id,
    start_time,
    time_passed_sec = 0;
var tick_event = function(){
        time_passed_sec += 1;
        $('.timer__value').text(
            getFormattedValue(time_passed_sec, 'h') + ':'
            + getFormattedValue(time_passed_sec, 'm') + ':'
            + getFormattedValue(time_passed_sec, 's')
        );
};
$('.js-start-count-form__start-button').on('click', function(){
    start_time = new Date();
    $(this).addClass('hidden');
    $('.js-start-count-form__action-type-select').prop('disabled', 'disabled');
    $('.js-start-count-form__pause-button').removeClass('hidden');
    $('.js-start-count-form__stop-button').removeClass('hidden');
    interval_id = setInterval(tick_event, 1000);
});
$('.js-start-count-form__pause-button').on('click', function(){
    clearInterval(interval_id);
    $(this).addClass('hidden');
    $('.js-start-count-form__resume-button').removeClass('hidden');
});
$('.js-start-count-form__resume-button').on('click', function(){
    interval_id = setInterval(tick_event, 1000);
    $(this).addClass('hidden');
    $('.js-start-count-form__pause-button').removeClass('hidden');
});
$('.js-start-count-form__stop-button').on('click', function(){
    var minutes_amount = time_passed_sec % 60,
        $actionTypeSelect = $('.js-start-count-form__action-type-select');
    $.ajax({
        type: 'POST',
        url: '/api/time_entry',  // FIXME hardcode url
        data: {
            action_type: $actionTypeSelect.val(),
            time_spend_min: minutes_amount
        },
        success: function(){
            var msg = 'Time entry "' + $('.js-start-count-form__action-type-select option:selected').text().trim() +
                ' - ' + minutes_amount + ' min" created.';
            $('.js-flash-container').noty({text: msg, type: 'success', timeout: 800});
            getStatistics($('.js-activity-chart').data('currentDays'), drawDonutGraph);
        },
        beforeSend: function(xhr, settings){
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
    clearInterval(interval_id);
    time_passed_sec = 0;
    $('.timer__value').text('');
    $actionTypeSelect.prop('disabled', '');
    $(this).addClass('hidden');
    $('.js-start-count-form__pause-button').addClass('hidden');
    $('.js-start-count-form__resume-button').addClass('hidden');
    $('.js-start-count-form__start-button').removeClass('hidden');
});
var formatNumberLength = function(num, length) {
    var r = "" + num;
    while (r.length < length) {
        r = "0" + r;
    }
    return r;
},
    getCookie = function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
    getFormattedValue = function(rawValue, valueId) {
        var value = null;
        if (valueId == 'h') {
            value = rawValue / 3600;
        }
        else if (valueId == 's') {
            value = rawValue % 60;
        }
        else if (valueId == 'm') {
            value = (rawValue % 3600) / 60;
        }

        return formatNumberLength(
            Math.floor(value),
            2
        );
};
