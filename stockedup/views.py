from django.shortcuts import render

def index(request):
	return render(request, 'stockedup/index.html')

def stock(request):
	return render(request, 'stockedup/stock.html')
