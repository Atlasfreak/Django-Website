function addForm(btn) {
    let button = $(btn);
    let form_id = button.attr('id');
    let form_total = parseInt($('#id_' + form_id + '-TOTAL_FORMS').val());
    let max_forms = parseInt($('#id_' + form_id + '-MAX_NUM_FORMS').val());
    
    if (form_total < max_forms) {
        let regex = new RegExp(form_id + '-__prefix__', 'g');
        button.before($('#' + form_id + '-empty').html().replaceAll(regex, form_id + '-' + form_total));
        $('#id_' + form_id + '-TOTAL_FORMS').val(form_total + 1);
    } else {
        button.popover({
            content: '<span class="text-danger">Du hast die maximale Anzahl an Feldern erreicht!</span>',
            trigger: 'hover',
            html: true,
        });
        button.popover('show');
    }
}

function removeForm(btn) {
    let button = $(btn);
    let form_id = button.attr('id');
    let data_target = button.data('target');
    let form_total = parseInt($('#id_' + form_id + '-TOTAL_FORMS').val());
    let min_forms = parseInt($('#id_' + form_id + '-MIN_NUM_FORMS').val());
    let btn_parent = button.parents(data_target);

    $('#' + form_id + '.add_form').popover('dispose');

    if (form_total > min_forms) {
        button.parentsUntil(data_target).remove();
        let children = btn_parent.children();

        for (let i=0, len=children.length; i<len; i++) {
            let regex = new RegExp(form_id + '-\\d+-', 'g');
            let replacement = form_id + '-' + i + '-';
            let replace = $(children.get(i)).html().replaceAll(regex, replacement);
            $(children.get(i)).html(replace);
        }

        $('#id_' + form_id + '-TOTAL_FORMS').val(form_total - 1);
    }
}

function changeAvailableOptions(origin, parent, options_id, values, message) {
    let target = $(origin);
    let val = parseInt(target.val());
    let options = target.parents(parent).find(options_id);

    if (values.includes(val)) {
        options.hide(0);
        if (!options.prev('div.options_unavailable').length) {
            options.before('<div class="options_unavailable">' + message + '</div>')
        }
    } else {
        if (options.prev('div.options_unavailable')) {
            options.prev('div.options_unavailable').remove();
        }
        options.show(0);
    }
}