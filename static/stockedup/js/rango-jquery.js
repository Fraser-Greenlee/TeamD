$(document).ready(function(){
    $("#login").hide();
    $("#signup").show();
    $("a.signup").click( function(event) {
    $("#login").hide();
    $("#signup").show();
    });
    $("a.login").click( function(event) {
    $("#login").show();
    $("#signup").hide();
    });
});