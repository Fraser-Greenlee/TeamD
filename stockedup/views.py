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
	# if logged in take to stock page
	if request.user.is_authenticated:
		return redirect('/stock')
	# else take to login page
	else:
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
	# insert user items into stock list of dicts
	items = Item.objects.filter(user=request.user)
	contextDict = {'stock': []}
	for item in items:
		contextDict['stock'] += [
			{'name': item.name, 'from': item.supplier, 'kgpw': item.rate, 'amount': item.stock, 'ppkg': 2}]
	# get upcomingOrders list
	contextDict['orders'] = upcomingOrdersList(items)
	#
	return render(request, 'stockedup/stock.html', context=contextDict)


@login_required
def ordertill(request):
	if request.method == 'POST':
		# take list of dicts from json string
		orders = json.loads(request.POST['ordertill'])
		emails = {}
		for item in orders:
			# update database item stock
			dbitem = Item.objects.filter(name=item['name'],user=request.user)[0]
			dbitem.stock += Decimal(item['amount'][:-2])
			dbitem.save()
			# make message to item supplier
			if item['fromemail'] not in emails:
				emails[item['fromemail']] = u"""
I would like to order,
"""
			emails[item['fromemail']] += u"""
{amount} of {name} for {cost}
""".format(**item)
		# make receipt message for user
		receipt = u'''Your last orders,
'''
		for address in emails.keys():
			# Not Sending to suppliers since we don't use real email addresses. Would be,
			# EmailMessage("Orders", emails[address], to=[address]).send()
			receipt += '''
---- '''+address+'''
'''+emails[address]
		# send receipt to user
		EmailMessage("Receipt", receipt, to=[request.user.email]).send()
	# - if sent a GET request just redirect the user
	# redirect to stock page
	return redirect('/stock')


@login_required
def upcomingorders(request):
	# use upcomingorders template to return only the html for the list
	contextDict = { 'orders' : upcomingOrdersList( Item.objects.filter(user=request.user) )  }
	return render(request, 'stockedup/upcomingorders.html', context=contextDict)


@login_required
def pred(request):
	# search tesco shopping api for a product of the same name,
	# taking only 1 result with no offset
	results = json.loads(requests.get('https://dev.tescolabs.com/grocery/products/?query=' + request.GET['name'] + '&offset=0&limit=1', headers={'Ocp-Apim-Subscription-Key': '14a1586c048a4159ad48693976e74894'}).content)['uk']['ghs']['products']['results'])
	if len(results) > 0:
		return HttpResponse(results[0]['unitprice'])
	else:
		return HttpResponse("None")


@login_required
def save(request):
	if request.method == 'GET':
		# d is of the form,
		# d = {'len':i,'data[0][amount]':amount,'data[0][ppkg]':val,,'data[i][amount]':amount,,}
		d = request.GET
		# get current user items
		olditems = Item.objects.filter(user=request.user)
		# delete all user items from the database
		delete_user_items(request)
		for i in range(int(d['len'])):
			# find/create item supplier + item
			s = Supplier.objects.get_or_create(name=get(d, i, 'from'), email=get(d, i, 'fromemail'))[0]
			item = Item.objects.get_or_create(user=request.user, name=get(d, i, 'name'), supplier=s)[0]
			item.stock = float(get(d, i, 'amount'))
			item.cost = float(get(d, i, 'ppkg'))
			# find item of same name in olditems
			previtems = olditems.filter(name=item.name)
			if len(previtems) > 0:
				previtem = previtem[0]
				# if found check rate has not been changed
				if float(get(d, i, 'kgpw')) != olditem.rate:
					print 'not equall', float(get(d, i, 'kgpw')), olditem.rate
					item.rate = float(get(d, i, 'kgpw'))
				else:
					# calculate new kg/week
					if olditem.stock > item.stock:
						weeksdff = (datetime.date.today() - olditem.lastUpdated).days()/7
						amountdff = olditem.stock - item.stock
						print 'weeksdff', weeksdff
						if weeksdff > 0 and amountdff > 0:
							print 'Updated Rate:', amountdff / weeksdff
							item.rate = amountdff / weeksdff
			# save item
			item.save()
		return HttpResponse("saved")
	else:
		return HttpResponse("must be GET request")


##	Functions for use in save

def get(data, i, k):
	return data[make_key(i, k)]

def make_key(i, k):
	return 'data[' + str(i) + '][' + k + ']'

def delete_user_items(request):
	Item.objects.filter(user=request.user).delete()

##
