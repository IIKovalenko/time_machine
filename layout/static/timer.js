var interval_id,
    start_time,
    hours = 0,
    minutes = 0,
    seconds = 0;
var tick_event = function(){
        seconds += 1;
        if(seconds > 59){
            seconds = 0;
            minutes += 1;
        }
        if(minutes > 59){
            minutes = 0;
            hours += 1;
        }

        $('.timer__value').text(
            formatNumberLength(hours, 2) + ':' + formatNumberLength(minutes, 2) + ':' + formatNumberLength(seconds, 2)
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
    var minutes_amount = hours * 60 + minutes,
        $actionTypeSecect = $('.js-start-count-form__action-type-select');
    $.ajax({
        type: 'POST',
        url: '/api/time_entry',  // FIXME hardcode url
        data: {
            action_type: $actionTypeSecect.val(),
            time_spend_min: hours * 60 + minutes
        },
        success: function(){
            var msg = 'Time entry "' + $('.js-start-count-form__action-type-select option:selected').text().trim() +
                ' - ' + minutes_amount + ' min" created.';
            $('.js-flash-container').noty({text: msg, type: 'success', timeout: 800});
        },
        beforeSend: function(xhr, settings){
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
    clearInterval(interval_id);
    hours = 0;
    minutes = 0;
    seconds = 0;
    $('.timer__value').text('');
    $actionTypeSecect.prop('disabled', '');
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
    };
