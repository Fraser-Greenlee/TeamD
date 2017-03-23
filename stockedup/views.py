# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from stockedup.models import Supplier, Item
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import EmailMessage
import datetime, json, requests
import pprint
from decimal import Decimal

def index(request):
	return redirect('/accounts/login/')

def upcomingOrdersList(items):
	OrderedOrders = []
	datedOrders = {}
	orders = []
	# Add all items that should be displayed at stock and for
	# any item whose rate is not 0 add them to a list of orders to be processed
	for item in items:
		if item.rate != 0:
			orders += [(int(item.stock / item.rate)*7, item)]  # Creates tuple: order = (Days Left, Item)
	orders = sorted(orders, key=lambda order: order[0])  # Sort by days lasting
	days = ("Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun")
	months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
	# Sorts the orders into a dictionary with keys of the day
	# of order in form ie. ['Mon 28 Jan'] which has all orders of the day
	for order in orders:
		orderDate = order[1].lastUpdated + datetime.timedelta(order[0])  # Find reorder date
		# Turns numerical date into text format
		stringDate = str(days[orderDate.weekday()]) + ' ' + str(orderDate.day) + ' ' + str(months[orderDate.month - 1])
		# Adds to dictionary in format {total, Orders[]}
		datedOrders[stringDate] = {'total': 0,
								   'orders': datedOrders.get(stringDate, {'orders': []})['orders'] + [
									   {'name': order[1].name,
										'from': order[1].supplier,
										'cost': round(order[1].cost * order[1].rate), 'amount': order[1].rate}]}
	# Takes each day adds it to array in format context wants for view
	for day in datedOrders:
		tempList = []
		total = 0
		for order in datedOrders[day]['orders']:
			total += order['cost']  # Sums up cost
			tempList += [order]
		OrderedOrders += [{'date': day, 'total': total, 'orders': tempList}]
	OrderedOrders = sorted(OrderedOrders, key=lambda k: k['date'].split(' ')[1])
	OrderedOrders = sorted(OrderedOrders, key=lambda k: (months.index(k['date'].split(' ')[2])))
	return OrderedOrders

@login_required
def stock(request):
	items = Item.objects.filter(user=request.user)
	contextDict = {'stock': [], 'orders': []}
	for item in items:
		contextDict['stock'] += [
			{'name': item.name, 'from': item.supplier, 'kgpw': item.rate, 'amount': item.stock, 'ppkg': 2}]
	contextDict['orders'] = upcomingOrdersList(items)
	return render(request, 'stockedup/stock.html', context=contextDict)

@login_required
def ordertill(request):
	if request.method == 'POST':
		orders = json.loads(request.POST['ordertill'])
		print orders
		emails = {}
		for item in orders:
			# [{"name":"Soup","amount":"5.00kg","cost":"£10.0","fromemail":"H@mail.com"}]
			dbitem = Item.objects.filter(name=item['name'],user=request.user)[0]
			dbitem.stock += Decimal(item['amount'][:-2])
			dbitem.save()
			if item['fromemail'] not in emails:
				emails[item['fromemail']] = u"""
I would like to order,
"""
			#
			emails[item['fromemail']] += u"""
{amount} of {name} for {cost}
""".format(**item)
		#
		receipt = u'''Your last orders,
'''
		for address in emails.keys():
			# Not Sending to suppliers since we don't have real addresses to send to. Would be,
			# EmailMessage("Orders", emails[address], to=[address]).send()
			receipt += '''
---- '''+address+'''
'''+emails[address]
	EmailMessage("Receipt", receipt, to=[request.user.email]).send()
	return redirect('/stock')


@login_required
def upcomingorders(request):
	contextDict = { 'orders' : upcomingOrdersList( Item.objects.filter(user=request.user) )  }
	return render(request, 'stockedup/upcomingorders.html', context=contextDict)


@login_required
def pred(request):
	return HttpResponse(json.loads(
		requests.get('https://dev.tescolabs.com/grocery/products/?query=' + request.GET['name'] + '&offset=0&limit=1',
					 headers={'Ocp-Apim-Subscription-Key': '14a1586c048a4159ad48693976e74894'}).content)['uk']['ghs'][
							'products']['results'][0]['unitprice'])


@login_required
def save(request):
	if request.method == 'GET':
		d = request.GET
		olditems = Item.objects.filter(user=request.user)
		delete_user_items(request)
		for i in range(int(d['len'])):
			s = Supplier.objects.get_or_create(name=get(d, i, 'from'), email=get(d, i, 'fromemail'))[0]
			item = Item.objects.get_or_create(user=request.user, name=get(d, i, 'name'), supplier=s)[0]
			item.stock = float(get(d, i, 'amount'))
			# find item of same names in olditems
			olditems.filter(name=item.name)
			if len(olditems) > 0:
				olditem = olditems[0]
				if float(get(d, i, 'kgpw')) != olditem.rate:
					print 'not equall', float(get(d, i, 'kgpw')), olditem.rate
					item.rate = float(get(d, i, 'kgpw'))
				else:
					if olditem.stock > item.stock:
						daysdff = (datetime.date.today() - olditem.lastUpdated).days()
						print 'daysdff', daysdff
						amountdff = olditem.stock - item.stock
						if daysdff > 0 and amountdff > 0:
							print 'Updated Rate:', amountdff / daysdff
							item.rate = amountdff / daysdff
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
