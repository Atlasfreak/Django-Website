function addHref(btn) {
    let href = $(btn).data('url');
    let modal_id = $(btn).data('bs-target');
    let link_id = $(modal_id).data('link-id');
    $(modal_id).find(link_id).attr('href', href);
}
$(document).ready(function () {
    $('main > div.container').on('click', '#delete', function () {
        addHref(this);
    });
});