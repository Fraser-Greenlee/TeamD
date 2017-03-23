# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from stockedup.models import Supplier, Item
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
import datetime, json, requests
import pprint
from decimal import Decimal

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
	contextDict['orders'] = sorted(contextDict['orders'], key=lambda k: months.index(k['date'].split(' ')[2]))
	return render(request, 'stockedup/stock.html', context=contextDict)

@login_required
def ordertill(request):
	if request.method == 'POST':
		orders = request.POST['ordertill'].split(',,')
		emails = {}
		for item in orders:
			# item = [u'potatoes', u'2.00', u'4.0', u'b@b.com']
			item = item.split(',')
			if len(item) < 4:
				continue
			it = Item.objects.filter(user=request.user,name=item[0])[0]
			it.stock += Decimal(item[1])
			it.save()
			#
			print item
			if item[3] not in emails:
				emails[item[3]] = """
Dear {name},

I would like to order,"""
			emails[item[3]] += """
{amount}kg of {name} for £{cost}""".format(amount=item[2], name=item[0], cost=item[1])
		#
		for address in emails.keys():
			try:
				send_mail("Orders", emails[address], request.user.email, [address])
			except Exception:
				print 'not sent'
	return redirect('/stock')

@login_required
def upcomingorders(request):
	if request.method == 'GET':
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
		sorted(orders, key=lambda order: order[0])  # Sort by days lasting
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
	return render(request, 'stockedup/upcomingorders.html', context=contextDict)

@login_required
def pred(request):
	return HttpResponse(json.loads(requests.get('https://dev.tescolabs.com/grocery/products/?query='+request.GET['name']+'&offset=0&limit=1', headers={'Ocp-Apim-Subscription-Key':'14a1586c048a4159ad48693976e74894'}).content)['uk']['ghs']['products']['results'][0]['unitprice'])

@login_required
def save(request):
	if request.method == 'GET':
		d = request.GET
		delete_user_items(request)
		for i in range(int(d['len'])):
			s = Supplier.objects.get_or_create(name=get(d, i, 'from'), email=get(d, i, 'fromemail'))[0]
			item = Item.objects.get_or_create(user=request.user, name=get(d, i, 'name'), supplier=s)[0]
			item.stock = float(get(d, i, 'amount'))
			item.rate = float(get(d, i, 'kgpw'))
			item.cost = float(get(d, i, 'ppkg'))
			item.save()
		return HttpResponse("saved")
	else:
		return HttpResponse("must be GET request")

def get(data, i, k):
	return data[make_key(i, k)]


def make_key(i, k):
	return 'data[' + str(i) + '][' + k + ']'


def delete_user_items(request):
	Item.objects.filter(user=request.user).delete()
