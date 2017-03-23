$(document).ready(function(){
	// get order select input options
	refreshOrderSelect();
	$("ul#additem").click( function(event) {
		// when click additem add a new item input field
		if ($("#currentStock").hasClass("edit")) {
			newHtml =  '<ul>';
			newHtml += '<p>name</p><input type="text" name="name">';
			newHtml += '<p>supplier</p><input type="text" name="from" placeholder="name"><input type="email" placeholder="email address" name="fromemail">';
			newHtml += '<p>amount (kg)</p><input type="number" name="amount">';
			newHtml += '<p>kg per week</p><input type="number" name="kgpw">';
			newHtml += '<p>price per kg<a class="pred">predict</a></p><input type="number" name="ppkg">';
			newHtml += '<a class="removelink">Remove</a>';
			newHtml +=  '</ul>';
			$(newHtml).insertBefore("#currentStock ul:last-child");
			// add link triggers
			EditItemTriggers();
		}
	});
	$("#sendorder").click(function(event) {
		// when click on Order show the order inputs
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
	// add trigger for edit button
	EditTrigger();
});

function EditTrigger() {
	// set trigger for edit button
	$("#currentStock a.edit").click( function(event) {
		$("#currentStock ul:not(#additem)").each(function(i) {
			// convert each stock item row value to edital inputs
			newHtml = '';
			newHtml += '<p>name</p><input type="text" name="name" value="'+$(this).children("[data-type='name']").text()+'">';
			newHtml += '<p>supplier</p><input type="text" name="from" value="'+$(this).children("[data-type='from']").text()+'"><input type="email" name="fromemail" value="'+$(this).attr('data-fromemail')+'">';
			newHtml += '<p>amount (kg)</p><input type="number" name="amount" value="'+$(this).children("[data-type='amount']").text().slice(0,-2)+'">';
			newHtml += '<p>kg per week</p><input type="number" name="kgpw" value="'+$(this).attr('data-kgpw')+'">';
			newHtml += '<p>price per kg<a class="pred">predict</a></p><input type="number" name="ppkg" value="'+$(this).attr('data-ppkg')+'">';
			newHtml += '<a class="removelink">Remove</a>';
			// replace ul html with new html
			$(this).html(newHtml);
		});
		// add link triggers
		EditItemTriggers();
		// reset current stock options and add triggers
		$("#currentStock > span").html('<h1>Stock</h1><a class="save">Save</a><a class="cancel">Cancel</a>');
		SaveCancelTriggers();
		// turn on edit mode
		$("#currentStock").addClass("edit");
	});
}

function EditItemTriggers() {
	// add remove link trigger
	$("#currentStock a.removelink").click( function(event) {
		$(this).parent().addClass("willRemove");
	});
	// add predict link trigger
	$(".pred").click(function(event) {
		box = $(this).parent().parent();
		$.get('/ajax/predict', {'name':$(box).children("[name='name']").val()}, function(data) {
			$(box).children("[name='ppkg']").val(data);
		});
	});
}

function SaveCancelTriggers() {
	$("#currentStock a.cancel").click( function(event) {
		// if click Cancel button
		$("#currentStock ul:not(#additem)").each(function(i) {
			// reset to old default values (as well as looping thorugh "removed" elements)
			newHtml = '';
			newHtml += '<span data-type="name">'+$(this).children("[name='name']").attr('value')+'</span>';
			newHtml += '<span data-type="from">'+$(this).children("[name='from']").attr('value')+'</span>';
			newHtml += '<span data-type="amount">'+$(this).children("[name='amount']").attr('value')+'kg</span>';
			$(this).html(newHtml);
		});
		resetStockOptions();
	});
	//
	$("#currentStock a.save").click( function(event) {
		// if click Save button
		// take all inputed values as list of dics
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
			// make display html
			newHtml = '';
			newHtml += '<span data-type="name">'+data.name+'</span>';
			newHtml += '<span data-type="from">'+data.from+'</span>';
			newHtml += '<span data-type="amount">'+data.amount+'kg</span>';
			$(this).html(newHtml);
			// set data attributes
			$(this).attr("data-kgpw",data.kgpw);
			$(this).attr("data-ppkg",data.ppkg);
			$(this).attr("data-fromemail",data.fromemail);
			// add to  newValues
			newValues.push(data);
		});
		// send newValues over ajax to update database
		$.get('/ajax/save', {'len':newValues.length, 'data': newValues}, function(data){
			if (data != 'saved') {
				alert('Error saving: '+data);
			}
			// reset order dates
			refreshUpcomingOrders();
		});
		resetStockOptions();
	});
}

function resetStockOptions() {
	// reset currentStock options
	$("#currentStock > span").html('<h1>Stock</h1><a class="edit">Edit</a>');
	// add trigger for edit button
	EditTrigger();
	// turn off edit mode
	$("#currentStock").removeClass("edit");
}

function refreshUpcomingOrders() {
	$.get('/ajax/upcomingorders', function(data) {
		$("#upcomingOrders > li").html(data);
		refreshOrderSelect();
	});
}

function refreshOrderSelect() {
	// reset order select input
	$("[name='ordertill']").html("");
	// go through each order day
	$("#upcomingOrders li h2 span:first-child").each(
		function(i) {
			// make list of ducts for each item to be ordered on that day
			orderInfo = [];
			orderElms = $($(this).parent().parent()[0]).find("li ul");
			for (i = 0; i < orderElms.length; i++) {
				children = $(orderElms[i]).find("span");
				orderInfo.push({
					name			:	children[0].innerText,
					amount		:	children[2].innerText,
					cost			:	children[1].innerText,
					fromemail : $(orderElms[i]).attr("data-fromemail")
				});
			}
			// turn orderInfo into json to be read by ordertill() in view.py
			$("[name='ordertill']").append($('<option>', {value: JSON.stringify(orderInfo),text: this.innerText}));
		}
	);
}
