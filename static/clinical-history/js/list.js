$(document).ready(function() {
    $('.select2').select2({
        theme:'bootstrap',
        language:'es'
    });

    load_all_registers();
    
    $('#id_patient').on('change', function() {
        id = $(this).val();
        if(id == '') {
            load_all_registers();
            return false;
        }
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
                {"data": "treatment"},
                {"data": "total"},
            ],
            columnDefs: [
                                
            ],
            initComplete: function (settings, json) {
    
            }
        });
    });

    function load_all_registers(){
        $('#tblAppointments').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'all',
                     'id':-1
                },
                dataSrc: ""
            },
            columns: [
                {"data": "id"},
                {"data": "date"},
                {"data": "doctor"},
                {"data": "patient"},
                {"data": "diagnostic"},
                {"data": "treatment"},
                {"data": "total"},
            ],
            columnDefs: [
                                
            ],
            initComplete: function (settings, json) {
    
            }
        });
    }
});