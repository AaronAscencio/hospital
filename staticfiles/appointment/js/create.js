$(document).ready(function() {
    $.datepicker.setDefaults($.datepicker.regional['es']);
    $("#id_date").datepicker({
        dateFormat: 'yy-mm-dd',
        maxDate: new Date(),
    });

    $('#id_time').timepicker({
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
