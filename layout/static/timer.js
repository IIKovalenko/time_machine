var interval_id,
    start_time,
    hours = 0,
    minutes = 0,
    seconds = 0,
    diff = null;
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
    console.log(diff);  // TODO send POST request and create time entry
    clearInterval(interval_id);
    diff = null;
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
}
