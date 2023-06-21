var tblSale;
$(function () {
    tblSale = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "name"},
            {"data": "curp"},
            {"data": "total"},
            {"data": "points"},
        ],
        columnDefs: [
            
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody').on('click', 'a[rel="details"]',function(){
        let tr = tblSale.cell($(this).closest('td,li')).index();
        let data = tblSale.row(tr.row).data();
        $("#myModalDet").modal('show');
        tblDet= $('#tblDet').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_details_prod',
                    'id':data.id,
                },
                dataSrc: ""
            },
            columns: [
                {"data": "prod.name"},
                {"data": "prod.cate.name"},
                {"data": "price"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-1, -3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                       return  data;
                    }
                },
            ],
            initComplete: function (settings, json) {
    
            }
        });
    });
});