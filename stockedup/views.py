from django.shortcuts import render
from stockedup.forms import SignUpForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

def index(request):

	registered = False

	if request.method == 'POST':
		signup_form = SignUpForm(data=request.POST)

		if signup_form.is_valid():
			user = signup_form.save()
			user.set_password(user.password)
			user.save()
			registered = True
			return render(request, 'stockedup/stock.html')
		else:
			print(signup_form.errors)
	else:
		signup_form = SignUpForm()

	return render(request, 'stockedup/index.html', {'signup_form': signup_form, 'registered': registered})

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
