$(document).ready(function(){
    // When signup text is clicked show signup form
    $("a.signup").click( function(event) {
			if ($("#authbox").hasClass("login")) {
				$("#authbox").addClass('signup').removeClass('login');
			}
    });
    // When login text is clicked show login form
    $("a.login").click( function(event) {
			if ($("#authbox").hasClass("signup")) {
				$("#authbox").addClass('login').removeClass('signup');
			}
    });
});
