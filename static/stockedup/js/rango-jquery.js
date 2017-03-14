$(document).ready(function(){
    //Settings
    var inFocusTextColor = "#fff"
    var outFocusTextColor = "rgba(255, 255, 255, 0.41)"

    // Initialisation

    // When signup text is clicked show signup form
    $("a.signup").click( function(event) {
        $("#login").hide();
        $("#signup").show();
        $(this).css('color', inFocusTextColor);
        $("a.login").css('color', outFocusTextColor);
    });
    // When login text is clicked show login form
    $("a.login").click( function(event) {
        $("#login").show();
        $("#signup").hide();
        $(this).css('color', inFocusTextColor);
        $("a.signup").css('color', outFocusTextColor);
    });
});