function updateInput(el: HTMLInputElement, replacement: string, id_regex: RegExp) {
    if ($(el).prop("for")) {
        $(el).prop("for", $(el).prop("for").replace(id_regex, replacement));
    }
    if (el.id) {
        el.id = el.id.replace(id_regex, replacement);
    }
    if (el.name) {
        el.name = el.name.replace(id_regex, replacement);
    }
}

function addForm(btn: string) {
    let button = $(btn);
    let form_id = button.attr("id");
    let form_total = Number($(`#id_${form_id}-TOTAL_FORMS`).val());
    let max_forms = Number($(`#id_${form_id}-MAX_NUM_FORMS`).val());

    if (form_total < max_forms) {
        let regex = new RegExp(`${form_id}-__prefix__`, "g");
        let prefix = `${form_id}-${form_total}`;
        button.before($(`#${form_id}-empty`).html().replaceAll(regex, prefix));
        $(`#id_${form_id}-TOTAL_FORMS`).val(form_total + 1);
    } else {
        button.popover({
            content: "<span class='text-danger'>Du hast die maximale Anzahl an Feldern erreicht!</span>",
            trigger: "hover",
            html: true,
        });
        button.popover("show");
    }
}

function removeForm(btn: string) {
    let button = $(btn);
    let form_id = button.attr("id");
    let data_target = button.data("target");
    let form_total = Number($(`#id_${form_id}-TOTAL_FORMS`).val());
    let min_forms = Number($(`#id_${form_id}-MIN_NUM_FORMS`).val());
    let btn_parent = button.parents(data_target);

    $(`#${form_id}.add_form`).popover("dispose");

    if (form_total > min_forms) {
        button.parentsUntil(data_target).remove();
        let children = btn_parent.children();
        const id_regex = new RegExp(`${form_id}-\\d+`, "g");
        for (let i = 0, len = children.length; i < len; i++) {
            let child = children.get(i);
            let replacement = `${form_id}-i`;
            updateInput(child, replacement, id_regex);
            $(child).find("*").each(function (this: HTMLInputElement) {
                updateInput(this, replacement, id_regex);
            });
        }

        $(`#id_${form_id}-TOTAL_FORMS`).val(form_total - 1);
    }
}

function changeAvailableParams(target: JQuery, options: JQuery, val: number) {
    const regex = new RegExp("[a-z]*-\\d+-", "gi");
    const param_regex = new RegExp("__prefix__-", "g");
    const ids_to_params = JSON.parse($("#param_ids_to_forms").text());
    let match = target.attr("name").match(regex);
    let prefix = match != null ? match[0] : "";
    let params_div = $("#question_type_params");

    options.prevUntil(".card-body").remove();
    if (val in ids_to_params) {
        let params = ids_to_params[val];
        params.forEach(param => {
            let input = params_div.find(`input[name=__prefix__-${param}]`);
            let copy_div = input.parentsUntil(params_div);

            if (!options.prevAll(`div.${param}`).length) {
                let copied = copy_div.clone().prependTo(options.parents(".card-body")).wrap(`<div class=${param}></div>`);
                if (params.indexOf(param) == 0) {
                    copied.append("<hr>");
                }
                copied[0].outerHTML = copied[0].outerHTML.replaceAll(param_regex, prefix);
            }

        });
    }
}

function changeAvailableOptions(origin: HTMLInputElement, parent: string, options_id: string, values: Array<number>, message: string) {
    const class_name = "options_unavailable";
    const html_tag = "h5";
    let target = $(origin);
    let val = parseInt(origin.value);
    let options = target.parents(parent).find(options_id);

    changeAvailableParams(target, options, val);
    if (values.includes(val) || isNaN(val)) {
        options.attr("hidden", "true");
        if (!options.prevAll(`${html_tag}.${class_name}`).length) {
            options.before(`<${html_tag} class='${class_name}'>${message}</${html_tag}>`);
        }
    } else {
        if (options.prevAll(`${html_tag}.${class_name}`)) {
            options.prevAll(`${html_tag}.${class_name}`).remove();
        }
        options.removeAttr("hidden");
    }
}

$(function () {
    const options_deactivated: number[] = JSON.parse($("#options_deactivated").text());
    const field_ids: Object = JSON.parse($("#field_ids").text());
    const question_type_selector = `#${field_ids["question_type"]} > select`;

    $(question_type_selector).each(function (this: HTMLInputElement) {
        changeAvailableOptions(this, ".card", ".options", options_deactivated, "Dieser Fragetyp lässt keine Auswahlmöglichkeiten zu.");
    });

    $("form").on("click", ".add_form", function () {
        addForm(this);
    });

    $("form").on("click", ".remove_form", function () {
        removeForm(this);
    });

    $("form").on("change", question_type_selector, function () {
        changeAvailableOptions(this, ".card", ".options", options_deactivated, "Dieser Fragetyp lässt keine Auswahlmöglichkeiten zu.");
    });
});