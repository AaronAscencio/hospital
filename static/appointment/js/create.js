$(document).ready(function() {
    var currentDate = new Date();

    // Sumar 3 meses a la fecha actual
    var maxDate = new Date();
    maxDate.setMonth(maxDate.getMonth() + 3);
    $.datepicker.setDefaults($.datepicker.regional['es']);
    $("#id_date").datepicker({
        dateFormat: 'yy-mm-dd',
        minDate: currentDate,
        maxDate: maxDate
    });

    $('#id_time').timepicker({
        minTime: '9',
        maxTime: '6:00pm',
        timeFormat: 'HH:mm', // Formato de hora deseado
        stepMinute: 30, // Intervalo de minutos permitido
        showSecond: false, // No mostrar segundos
        controlType: 'select' // Mostrar selectores para cada componente de la hora
      });

    $('#id_doctor').addClass('select2');
    $('#id_nurse').addClass('select2');
    $('#id_patient').addClass('select2');

    $('.select2').select2({
        theme:'bootstrap',
        language:'es'
    });
});
