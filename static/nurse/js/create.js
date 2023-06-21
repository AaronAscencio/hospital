$(document).ready(function() {
    const avaliableDate = new Date();
    avaliableDate.setFullYear(avaliableDate.getFullYear() - 18);

    $.datepicker.setDefaults($.datepicker.regional['es']);
    $("#id_birthday_date").datepicker({
        dateFormat: 'yy-mm-dd',
        maxDate: avaliableDate,
        minDate: new Date(1920, 0, 1),
    });
});
