$(document).ready(function() {
    $.datepicker.setDefaults($.datepicker.regional['es']);
    $("#id_birthday_date").datepicker({
        dateFormat: 'yy-mm-dd',
        maxDate: new Date(),
        minDate: new Date(1920, 0, 1),
    });
});
