

$('.brand_name').on('click', function () {
    var checkbox_value = [];
    $(':checkbox').each(function () {
        var ischecked  = $(this).is(':checked');
        if(ischecked){
            checkbox_value.push($(this).val());
        }
    });
   $.ajax({
       url: '/ajax-search/',
       type: 'GET',
       data: {
           'brand_name': checkbox_value
       },
       success: searchSuccess,
       error: searchError
   })
});

function searchSuccess(data, textStatus, jqXHR) {
    console.log('works!');
    $('.product-list').empty().html(data)

}

function searchError(data, textStatus, jqXHR) {
    console.log('Error')
}



