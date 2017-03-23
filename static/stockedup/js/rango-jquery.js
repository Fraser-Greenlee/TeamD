$(document).ready(function(){
	$("ul#additem").click( function(event) {
		if ($("#currentStock").hasClass("edit")) {
			newHtml =  '<ul>';
			newHtml += '<p>name</p><input type="text" name="name">';
			newHtml += '<p>supplier</p><input type="text" name="from" placeholder="name"><input type="email" placeholder="email address" name="fromemail">';
			newHtml += '<p>amount (kg)<a class="pred">predict</a></p><input type="number" name="amount">';
			newHtml += '<p>kg per week</p><input type="number" name="kgpw">';
			newHtml += '<p>price per kg</p><input type="number" name="ppkg">';
			newHtml += '<a class="removelink">Remove</a>';
			newHtml +=  '</ul>';
			$(newHtml).insertBefore("#currentStock ul:last-child");
			RemoveTriggers();
		}
	});
	$("#sendorder").click(function(event) {
		if ($("#sendorder").hasClass("cancelorder")) {
			$("#inputorder").removeClass("show");
			$("#sendorder").removeClass("cancelorder");
			$("#sendorder").html("Order");
		} else {
			$("#inputorder").addClass("show");
			$("#sendorder").addClass("cancelorder");
			$("#sendorder").html("Cancel");
		}
	});
	$("orderbut").click(function(event) {
		before = $("[name='ordertill']").val();
		window.location.replace("http://127.0.0.1:8000/");
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
			newHtml += '<p>price per kg<a class="pred">predict</a></p><input type="number" name="ppkg" value="'+$(this).attr('data-ppkg')+'">';
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
	$(".pred").click(function(event) {
		box = $(this).parent().parent();
		$.get('ajax/predict', {'name':$(box).children("[name='name']").val()}, function(data) {
			console.log("data");
			console.log(data);
			$(box).children("[name='ppkg']").val(data);
		});
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
		$("#currentStock ul:not(#additem):not(.willRemove)").each(function(i) {
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
			refreshUpcomingOrders();
		});
		// TODO refresh upcoming orders after
		$("#currentStock > span").html('<h1>Stock</h1><a class="edit">Edit</a>');
		EditTrigger();
		$("#currentStock").removeClass("edit");
	});
}

function refreshUpcomingOrders() {
	$.get('ajax/upcomingorders', function(data) {
		$("#upcomingOrders > li").html(data);
	});
}
