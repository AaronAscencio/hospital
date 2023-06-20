$(document).ready(function() {
    $('#id_doctor').on('change', function() {
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
                {"data": "office.number"},
                {"data": "patient"},
                {"data": "doctor"},
                {"data": "nurse"},
                {"data": "date"},
                {"data": "time"},
                {"data": "specialty"},
            ],
            columnDefs: [
                                
            ],
            initComplete: function (settings, json) {
    
            }
        });
    });
});