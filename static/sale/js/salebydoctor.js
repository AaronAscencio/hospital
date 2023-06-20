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
                {"data": "date_joined"},
                {"data": "cli"},
                {"data": "doctor"},
                {"data": "diagnostic"},
                {"data": "treatment"},
                {"data": "specialty"},
                {"data": "id"},
            ],
            columnDefs: [
                
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '';
                        buttons += '<a href="/sale/invoice/pdf/'+row.id+'/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                        return buttons;
                    }
                }
            ],
            initComplete: function (settings, json) {
    
            }
        });
    });
});