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

        for (let i = 0, len = children.length; i < len; i++) {
            let regex = new RegExp(form_id + '-\\d+-', 'g');
            let replacement = form_id + '-' + i + '-';
            let replace = $(children.get(i)).html().replaceAll(regex, replacement);
            $(children.get(i)).html(replace);
        }

        $('#id_' + form_id + '-TOTAL_FORMS').val(form_total - 1);
    }
}

function changeAvailableParams(target, options, val) {
    const regex = new RegExp('[a-z]*-\\d+-', 'gi');
    const param_regex = new RegExp('__prefix__-', 'g')
    const ids_to_params = JSON.parse($('#param_ids_to_forms').text());
    let prefix = target.attr('name').match(regex);
    let params_div = $('#question_type_params');

    let before_options = options.prevUntil('.card-body').filter(function (index) {
        let array = Object.values(ids_to_params).flat(1);
        if (array.includes($(this).attr('class'))) {
            return true;
        }
        return false;
    });

    if (val in ids_to_params) {
        let params = ids_to_params[val];
        params.forEach(param => {
            let input = params_div.find('input[name=__prefix__-' + param + ']');
            let copy_div = input.parents('.form-group');

            if (!options.prevAll('div.' + param).length) {
                let copied = copy_div.clone().prependTo(options.parents('.card-body')).wrap('<div class=' + param + '></div>');
                if (params.indexOf(param) == 0) {
                    copied.append('<hr>');
                }
                copied[0].outerHTML = copied[0].outerHTML.replaceAll(param_regex, prefix);
            }

        });
    } else if (before_options) {
        $(before_options).remove();
    }
}

function changeAvailableOptions(origin, parent, options_id, values, message) {
    const class_name = 'options_unavailable'
    const html_tag = 'h5'
    let target = $(origin);
    let val = parseInt(target.val());
    let options = target.parents(parent).find(options_id);

    changeAvailableParams(target, options, val)
    if (values.includes(val)) {
        options.hide(0);
        if (!options.prevAll(html_tag + '.' + class_name).length) {
            options.before('<' + html_tag + ' class="' + class_name + '">' + message + '</' + html_tag + '>')
        }
    } else {
        if (options.prevAll(html_tag + '.' + class_name)) {
            options.prevAll(html_tag + '.' + class_name).remove();
        }
        options.show(0);
    }
}

$(document).ready(function () {
    const options_deactivated = JSON.parse($('#options_deactivated').text())
    $('.custom-select').each(function () {
        changeAvailableOptions(this, '.card', '#options', options_deactivated, 'Dieser Fragetyp lässt keine Auswahlmöglichkeiten zu.');
    });

    $('form').on('click', '.add_form', function () {
        addForm(this);
    });

    $('form').on('click', '.remove_form', function () {
        removeForm(this);
    });

    $('form').on('change', '.custom-select', function () {
        changeAvailableOptions(this, '.card', '#options', options_deactivated, 'Dieser Fragetyp lässt keine Auswahlmöglichkeiten zu.')
    });
});