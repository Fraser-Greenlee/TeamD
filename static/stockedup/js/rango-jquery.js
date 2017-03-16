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
		EditTrigger();
});

function EditTrigger() {
	$("#currentStock a.edit").click( function(event) {
		$("#currentStock ul:not(#additem)").each(function(i) {
			newHtml = '';
			$(this).children("span").each(function(i) {
				newHtml += '<input type="text" name="'+$(this).attr("data-type")+'" placeholder="'+$(this).attr("data-type")+'" value="'+$(this).text()+'">';
			});
			newHtml += '<a class="removelink">Remove</a>';
			$(this).html(newHtml);
		});
		RemoveTriggers();
		$("#currentStock > span").html('<h1>Stock</h1><a class="save">Save</a><a class="cancel">Cancel</a>');
		SaveCancelTriggers();
		$("#currentStock").addClass("edit");
	});
}

function RemoveTriggers() {
	$("#currentStock a.removelink").click( function(event) {
		$(this).parent().addClass("willRemove");
	});
}

function SaveCancelTriggers() {
	$("#currentStock a.cancel").click( function(event) {
		$("#currentStock ul:not(#additem)").each(function(i) {
			newHtml = '';
			$(this).children("input").each(function(i) {
				newHtml += '<span data-type="'+$(this).attr('name')+'">'+$(this).attr('value')+'</span>';
			});
			$(this).html(newHtml);
			$(this).removeClass("willRemove");
		});
		$("#currentStock > span").html('<h1>Stock</h1><a class="edit">Edit</a>');
		EditTrigger();
		$("#currentStock").removeClass("edit");
	});
	// save then display input values
	$("#currentStock a.save").click( function(event) {
		console.log('not implimented');
	});
}
