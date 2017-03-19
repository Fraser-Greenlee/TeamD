from django.shortcuts import render, redirect

def index(request):
	return redirect('/accounts/login/')

def stock(request):
	# sample data
	return render(request, 'stockedup/stock.html', context={
		'stock':[{'name':'Salad','from':'Harry Farms','kgmo':1.3,'amount':5,'ppkg':2},{'name':'Carrots','from':'Harry Farms','kgmo':3.1,'amount':5,'ppkg':2}],
		'orders':[
			{
				'date':'Fri 26 Nov','total':26,'orders':[{'name':'Salad','from':'Harry Farms','cost':30,'amount':10}]
			}
		]
	})
