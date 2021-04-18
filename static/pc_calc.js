$(function() {
    $('.btn-clear-all').click(function () {
        $( "input.element-input" ).each(function( index ) {
            $(this).val('');
        });
        $( "button.btn-set-mask.btn-set-unk" ).each(function( index ) {
            $(this).click();
        });

    });

    $('.btn-set-mask').click(function () {
        row_name = $(this).data("row");
        btn_type = $(this).data('btn-type');
        selector = 'input.' + row_name + '.' + btn_type;
        console.log('Clicking on button for ' + selector);
        checkboxes = $(selector);
        console.log(checkboxes.length.toString() + ' buttons found');
        for (var i = 0; i < checkboxes.length; i++) {
            console.log('getting box ' + i.toString());
             console.log('setting checked');
             checkboxes[i].checked = true;
         }
    });
});
