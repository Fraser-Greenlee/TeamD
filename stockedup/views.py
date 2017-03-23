from django.shortcuts import render, redirect
from stockedup.models import Supplier, Item
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
import pprint


def index(request):
	return redirect('/accounts/login/')

@login_required
def stock(request):
	currentUser = request.user
	items = filter(lambda x: x.user == currentUser, Item.objects.all())  # Filters items to only the current user
	contextDict = {'stock': [], 'orders': []}
	datedOrders = {}
	orders = []
	# Add all items that should be displayed at stock and for
	# any item whose rate is not 0 add them to a list of orders to be processed
	for item in items:
		contextDict['stock'] += [
			{'name': item.name, 'from': item.supplier, 'kgpw': item.rate, 'amount': item.stock, 'ppkg': 2}]
		if item.rate != 0:
			orders += [(int(item.stock / item.rate), item)]  # Creates tuple: order = (Days Left, Item)
	orders = sorted(orders, key=lambda order: order[0])  # Sort by days lasting
	days = ("Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun")
	months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
	# Sorts the orders into a dictionary with keys of the day
	# of order in form ie. ['Mon 28 Jan'] which has all orders of the day
	for order in orders:
		orderDate = datetime.date.today() + datetime.timedelta(order[0])  # Find reorder date
		# Turns numerical date into text format
		stringDate = str(days[orderDate.weekday()]) + ' ' + str(orderDate.day) + ' ' + str(months[orderDate.month - 1])
		# Adds to dictionary in format {total, Orders[]}
		datedOrders[stringDate] = {'total': 0,
								   'orders': datedOrders.get(stringDate, {'orders': []})['orders'] + [
									   {'name': order[1].name,
										'from': order[1].supplier,
										'cost': round(order[1].cost*order[1].rate), 'amount': order[1].rate}]}
	# Takes each day adds it to array in format context wants for view
	for day in datedOrders:
		tempList = []
		total = 0
		for order in datedOrders[day]['orders']:
			total += order['cost']  # Sums up cost
			tempList += [order]
		contextDict['orders'] += [{'date': day, 'total': total, 'orders': tempList}]
		# sample data
	contextDict['orders'] = sorted(contextDict['orders'], key=lambda k: months.index(k['date'].split(' ')[2]))
	#contextDict['orders'] = sorted(contextDict['orders'], key=lambda k: k['date'].split(' ')[1])
	pprint.pprint(contextDict)
	return render(request, 'stockedup/stock.html', context=contextDict)

@login_required
def ordertill(request):
	if request.method == 'POST':
		print request.POST['ordertill']
		return HttpResponse("a")

@login_required
def save(request):
	if request.method == 'GET':
		d = request.GET
		print 'd:', d
		delete_user_items(request)
		for i in range(int(d['len'])):
			s = Supplier.objects.get_or_create(name=get(d, i, 'from'), email=get(d, i, 'fromemail'))[0]
			item = Item.objects.get_or_create(user=request.user, name=get(d, i, 'name'), supplier=s)[0]
			item.stock = float(get(d, i, 'amount'))
			item.rate = float(get(d, i, 'kgpw'))
			item.cost = float(get(d, i, 'ppkg'))
			item.save()
		return HttpResponse("saved")
	return HttpResponse("must be POST request")


def get(data, i, k):
	return data[make_key(i, k)]


def make_key(i, k):
	return 'data[' + str(i) + '][' + k + ']'


def delete_user_items(request):
	Item.objects.filter(user=request.user).delete()
