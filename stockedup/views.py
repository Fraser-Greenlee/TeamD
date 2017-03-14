from django.shortcuts import render

def index(request):
	return render(request, 'stockedup/index.html')

def stock(request):
	# sample data
	return render(request, 'stockedup/stock.html', context={
		'stock':[{'name':'Salad','from':'Harry Farms','kgmo':1.3,'amount':5,'ppkg':2}],
		'orders':[
			{
				'date':'Fri 26 Nov','total':26,'orders':[{'name':'Salad','from':'Harry Farms','cost':30,'amount':10}]
			}
		]
	})
