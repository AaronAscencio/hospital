$(document).ready(function() {
    $('.select2').select2({
        theme:'bootstrap',
        language:'es'
    });

    
    $('#id_patient').on('change', function() {
        id = $(this).val();
        if(id == '') return false;
        $('#tblAppointments').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'searchdata',
                    'id':id
                },
                dataSrc: ""
            },
            columns: [
                {"data": "id"},
                {"data": "date"},
                {"data": "doctor"},
                {"data": "patient"},
                {"data": "diagnostic"},
                {"data": "sale.treatment"},
                {"data": "sale.total"},
            ],
            columnDefs: [
                                
            ],
            initComplete: function (settings, json) {
    
            }
        });
    });
});