// custom js functions
function back_to_top(){
    let btn = $("button#back-to-top")

    $(window).scroll(function() {
        if ( $(this).scrollTop() > 300 ) {
            btn.fadeIn();
        } else {
            btn.fadeOut();
        }
    });

    btn.click(function() {
        $("html, body").animate({
            scrollTop: 0
        }, 700);
        return false;
    });

}

function cookie_banner(){
    let keyvalue = document.cookie.match("(^|;) ?cookie_consent=([^;]*)(;|$)");
    let cookie_consentCookie = keyvalue ? decodeURIComponent(keyvalue[2]) : null;

    if (cookie_consentCookie) return;
    else {
        $(".cookie-consent").removeClass("hidden")
    }

    $(".cookie-consent-accept").click( function(){
        let max_age = (365*24*60*60);
        cookie_message = "accepted"
        document.cookie = `cookie_consent=${encodeURIComponent(cookie_message)}; max-age=${max_age};`
        location.reload();
    });

}

$(document).ready(function() {
    bsCustomFileInput.init()

    //back to top button
    back_to_top();

    //cookie banner
    cookie_banner();
});
