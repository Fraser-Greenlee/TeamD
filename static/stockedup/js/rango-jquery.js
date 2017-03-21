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
			newHtml += '<p>name</p><input type="text" name="name" value="'+$(this).children("[data-type='name']").text()+'">';
			newHtml += '<p>supplier</p><input type="text" name="from" value="'+$(this).children("[data-type='from']").text()+'"><input type="email" name="fromemail" value="'+$(this).attr('data-fromemail')+'">';
			newHtml += '<p>amount (kg)</p><input type="number" name="amount" value="'+$(this).children("[data-type='amount']").text().slice(0,-2)+'">';
			newHtml += '<p>kg per week</p><input type="number" name="kgpw" value="'+$(this).attr('data-kgpw')+'">';
			newHtml += '<p>price per kg</p><input type="number" name="ppkg" value="'+$(this).attr('data-ppkg')+'">';
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
			newHtml += '<span data-type="name">'+$(this).children("[name='name']").attr('value')+'</span>';
			newHtml += '<span data-type="from">'+$(this).children("[name='from']").attr('value')+'</span>';
			newHtml += '<span data-type="amount">'+$(this).children("[name='amount']").attr('value')+'kg</span>';
			$(this).html(newHtml);
		});
		$("#currentStock > span").html('<h1>Stock</h1><a class="edit">Edit</a>');
		EditTrigger();
		$("#currentStock").removeClass("edit");
	});
	//
	$("#currentStock a.save").click( function(event) {
		newValues = [];
		$("#currentStock ul:not(#additem)").each(function(i) {
			data = {
				'name':$(this).children("[name='name']").val(),
				'from':$(this).children("[name='from']").val(),
				'fromemail':$(this).children("[name='fromemail']").val(),
				'amount':$(this).children("[name='amount']").val(),
				'kgpw':$(this).children("[name='kgpw']").val(),
				'ppkg':$(this).children("[name='ppkg']").val()
			};
			newHtml = '';
			newHtml += '<span data-type="name">'+data.name+'</span>';
			newHtml += '<span data-type="from">'+data.from+'</span>';
			newHtml += '<span data-type="amount">'+data.amount+'kg</span>';
			$(this).html(newHtml);
			$(this).attr("data-kgpw",data.kgpw);
			$(this).attr("data-ppkg",data.ppkg);
			$(this).attr("data-fromemail",data.fromemail);
			newValues.push(data);
		});
		$.get('/ajax/save', {'len':newValues.length, 'data': newValues}, function(data){
			if (data != 'saved') {
				alert('Error saving: '+data);
			}
		});
		// TODO refresh upcoming orders after
		$("#currentStock > span").html('<h1>Stock</h1><a class="edit">Edit</a>');
		EditTrigger();
		$("#currentStock").removeClass("edit");
	});
}
