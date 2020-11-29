function addForm(btn) {
    form_id = $(btn).attr('id');
    form_total = $('#id_' + form_id + '-TOTAL_FORMS').val();

    console.log(form_id + ' val: ' + form_total);

    regex = new RegExp(form_id + '-__prefix__', 'g');
    $(btn).before($('#' + form_id + '-empty').html().replaceAll(regex, form_id + '-' + form_total));
    $('#id_' + form_id + '-TOTAL_FORMS').val(parseInt(form_total) + 1);
}