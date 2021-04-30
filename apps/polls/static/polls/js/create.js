function updateInput(el, replacement, id_regex) {
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
function checkUpdateQuestions(btn) {
    let update_questions_data = btn.data("updateQuestions");
    let update_questions = (typeof update_questions_data !== "undefined") ? JSON.parse(update_questions_data) : false;
    return update_questions;
}
function addForm(btn) {
    let button = $(btn);
    let form_id = button.attr("id");
    let form_total = Number($("#id_" + form_id + "-TOTAL_FORMS").val());
    let max_forms = Number($("#id_" + form_id + "-MAX_NUM_FORMS").val());
    const update_questions = checkUpdateQuestions(button);
    if (form_total < max_forms) {
        let regex = new RegExp(form_id + "-__prefix__", "g");
        let prefix = form_id + "-" + form_total;
        button.before($("#" + form_id + "-empty").html().replaceAll(regex, prefix));
        $("#id_" + form_id + "-TOTAL_FORMS").val(form_total + 1);
        if (update_questions) {
            updateQuestionJSON(prefix);
            updateRelatedQuestions(".options");
        }
    }
    else {
        button.popover({
            content: "<span class='text-danger'>Du hast die maximale Anzahl an Feldern erreicht!</span>",
            trigger: "hover",
            html: true,
        });
        button.popover("show");
    }
}
function removeForm(btn) {
    let button = $(btn);
    let form_id = button.attr("id");
    let data_target = button.data("target");
    let form_total = Number($("#id_" + form_id + "-TOTAL_FORMS").val());
    let min_forms = Number($("#id_" + form_id + "-MIN_NUM_FORMS").val());
    let btn_parent = button.parents(data_target);
    const update_questions = checkUpdateQuestions(button);
    $("#" + form_id + ".add_form").popover("dispose");
    if (form_total > min_forms) {
        button.parentsUntil(data_target).remove();
        let children = btn_parent.children();
        const id_regex = new RegExp(form_id + "-\\d+", "g");
        if (update_questions) {
            resetQuestionsStorage();
        }
        for (let i = 0, len = children.length; i < len; i++) {
            let child = children.get(i);
            let replacement = form_id + "-" + i;
            updateInput(child, replacement, id_regex);
            $(child).find("*").each(function () {
                updateInput(this, replacement, id_regex);
            });
            if (update_questions) {
                updateQuestionJSON(replacement);
            }
        }
        if (update_questions) {
            updateRelatedQuestions(".options", true);
        }
        $("#id_" + form_id + "-TOTAL_FORMS").val(form_total - 1);
    }
}
function changeAvailableParams(target, options, val) {
    const regex = new RegExp("[a-z]*-\\d+-", "gi");
    const param_regex = new RegExp("__prefix__-", "g");
    const ids_to_params = JSON.parse($("#param_ids_to_forms").text());
    let match = target.attr("name").match(regex);
    let prefix = match != null ? match[0] : "";
    let params_div = $("#question_type_params");
    options.prevUntil(".card-body").remove();
    if (val in ids_to_params) {
        let params = ids_to_params[val];
        params.forEach((param) => {
            let input = params_div.find("input[name=__prefix__-" + param + "]");
            let copy_div = input.parents(".form-group");
            if (!options.prevAll("div." + param).length) {
                let copied = copy_div.clone().prependTo(options.parents(".card-body")).wrap("<div class=" + param + "></div>");
                if (params.indexOf(param) == 0) {
                    copied.append("<hr>");
                }
                copied[0].outerHTML = copied[0].outerHTML.replaceAll(param_regex, prefix);
            }
        });
    }
}
function changeAvailableOptions(origin, parent, options_id, values, message) {
    const class_name = "options_unavailable";
    const html_tag = "h5";
    let target = $(origin);
    let val = parseInt(origin.value);
    let options = target.parents(parent).find(options_id);
    changeAvailableParams(target, options, val);
    if (values.includes(val) || isNaN(val)) {
        options.attr("hidden", "true");
        if (!options.prevAll(html_tag + "." + class_name).length) {
            options.before(`<${html_tag} class="${class_name}">${message}</${html_tag}>`);
        }
    }
    else {
        if (options.prevAll(html_tag + "." + class_name)) {
            options.prevAll(html_tag + "." + class_name).remove();
        }
        options.removeAttr("hidden");
    }
}
function addQuestionsToStorage(json) {
    const sortObject = obj => Object.keys(obj).sort().reduce((res, key) => (res[key] = obj[key], res), {});
    localStorage.setItem("questions", JSON.stringify(sortObject(json)));
}
function resetQuestionsStorage() {
    localStorage.setItem("questions", "{}");
}
function getStoredQuestions() {
    let stored_questions = localStorage.getItem("questions");
    if (stored_questions === null) {
        stored_questions = "{}";
    }
    return JSON.parse(stored_questions);
}
function getValueAndIDFromQuestion(prefix) {
    const question_text_id = JSON.parse($("#field_ids").text())["question_text"];
    let value = $("#id_" + prefix + "-" + question_text_id).val();
    let current_questions = null;
    if (typeof value !== "undefined") {
        current_questions = getStoredQuestions();
    }
    return [value, current_questions];
}
function updateQuestionJSON(prefix) {
    if (!/\S+-\d+/.test(prefix)) {
        return;
    }
    let [value, current_questions] = getValueAndIDFromQuestion(prefix);
    if (current_questions !== null) {
        current_questions[prefix] = value;
        addQuestionsToStorage(current_questions);
    }
}
function generateQuestionText(question, text) {
    const question_number = Number(question.replace("question-", "")) + 1;
    return "Frage " + question_number + ": " + text;
}
function getCurrentQuestion(el) {
    const question_regex = RegExp("question-\\d+");
    const question_match = question_regex.exec(el.id);
    const question = (question_match !== null) ? question_match[0] : "";
    return question;
}
function initUpdateFunctions(select_el, json_questions) {
    const options = select_el.options;
    const questions = $.extend({}, json_questions);
    const question = getCurrentQuestion(select_el);
    return { options, questions, question };
}
function loopOptions(options, ifFunction) {
    $.each(options, function (option_index) {
        let option = options[option_index];
        let value = option.value;
        if (value !== "") {
            ifFunction(option, value, option_index);
        }
    });
}
function updateOrAddRelatedQuestion(select_el, json_questions) {
    let { options, questions, question } = initUpdateFunctions(select_el, json_questions);
    delete questions[question];
    let options_removed = [];
    let ifFunc = (option, value, ...rest) => {
        if (value in questions) {
            option.text = generateQuestionText(value, questions[value]);
            delete questions[value];
        }
        else {
            options_removed.push(option);
        }
    };
    loopOptions(options, ifFunc);
    options_removed.forEach(function (option) {
        option.remove();
    });
    for (const key in questions) {
        let text = generateQuestionText(key, questions[key]);
        options[options.length] = new Option(text, key);
    }
}
function renumberRelatedQuestions(select_el, json_questions) {
    let { options, questions, question } = initUpdateFunctions(select_el, json_questions);
    const n_question_regex = /\d+/.exec(question);
    const question_number = (n_question_regex !== null) ? Number(n_question_regex[0]) : NaN;
    let ifFunc = (option, value, index) => {
        if (value.replace("question-", "") == String(question_number)) {
            option.remove();
            return;
        }
        if (index >= question_number) {
            index++;
        }
        option.value.replace(/\d+/, String(index));
        option.text = generateQuestionText(value, questions[value]);
    };
    loopOptions(options, ifFunc);
}
function updateRelatedQuestions(options_selector, removed = false) {
    let dom_options = $(options_selector);
    const related_question_id = "[id=" + JSON.parse($("#field_ids").text())["related_question"] + "]";
    let json_questions = getStoredQuestions();
    let updateFunction = updateOrAddRelatedQuestion;
    dom_options.each(function () {
        $(this).find(related_question_id + " > select").each(function () { updateFunction(this, json_questions); });
    });
}
$(document).ready(function () {
    const options_deactivated = JSON.parse($("#options_deactivated").text());
    const field_ids = JSON.parse($("#field_ids").text());
    const question_type_selector = "#" + field_ids["question_type"] + " > select";
    const question_text_selector = ".question > #" + field_ids["question_text"] + " > input";
    resetQuestionsStorage();
    $(question_type_selector).each(function () {
        changeAvailableOptions(this, ".card", ".options", options_deactivated, "Dieser Fragetyp lässt keine Auswahlmöglichkeiten zu.");
        let prefix = this.name.replace("-" + field_ids["question_type"], "");
        updateQuestionJSON(prefix);
        updateRelatedQuestions(".options");
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
    let question_timeout = null;
    $("form").on("keyup", question_text_selector, function () {
        clearTimeout(question_timeout);
        let prefix = this.name.replace("-" + field_ids["question_text"], "");
        question_timeout = setTimeout(function () {
            updateQuestionJSON(prefix);
            updateRelatedQuestions(".options");
        }, 500);
    });
});
//# sourceMappingURL=create.js.map