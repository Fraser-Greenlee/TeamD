from django.shortcuts import render, redirect
from stockedup.models import Supplier, Item
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime


def index(request):
    return redirect('/accounts/login/')


def stock(request):
    currentUser = request.user
    items = filter(lambda x: x.user == currentUser, Item.objects.all())  # Filters items to only the current user
    contextDict = {'stock': [], 'orders': []}
    datedOrders = {}
    orders = []
    for item in items:
        contextDict['stock'] += [{'name': item.name, 'from': item.supplier, 'kgpw': 1, 'amount': item.stock, 'ppkg': 2}]
        orders += [(int(item.stock / item.rate), item)]
    sorted(orders, key=lambda order: order[0])  # Sort by days lasting
    days = ("Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun")
    months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    for order in orders:
        orderDate = datetime.date.today() + datetime.timedelta(order[0])
        stringDate = str(days[orderDate.weekday()]) + ' ' + str(orderDate.day) + ' ' + str(months[orderDate.month - 1])
        datedOrders[stringDate] = {'total': 0,
                                   'orders': datedOrders.get(stringDate, {'orders': []})['orders'] + [
                                       {'name': order[1].name,
                                        'from': order[1].supplier,
                                        'cost': 30, 'amount': order[1].rate*7}]}

    for day in datedOrders:
        tempList = []
        total = 0
        for order in datedOrders[day]['orders']:
            total += order['cost']
            tempList += [order]
        contextDict['orders'] += [{'date': day, 'total': total, 'orders': tempList}]

            # sample data
    return render(request, 'stockedup/stock.html', context=contextDict)

@login_required
def save(request):
	if request.method == 'GET':
		delete_user_items(request)
		d = request.GET
		for i in range(int(d['len'])):
			s = Supplier.objects.get_or_create(name=get(d,i,'from'), email=get(d,i,'fromemail'))[0]
			item = Item.objects.get_or_create(user=request.user, name=get(d,i,'name'), supplier=s)[0]
			item.stock = float(get(d, i, 'amount'))
			item.rate =  float(get(d, i, 'kgpw'))
			item.cost =  float(get(d, i, 'ppkg'))
			item.save()
		return HttpResponse("saved")
	return HttpResponse("must be GET request")

def get(data,i,k):
	return data[make_key(i,k)]

def make_key(i,k):
	return 'data['+str(i)+']['+k+']'

def delete_user_items(request):
	print Item.objects.filter(user=request.user)
	Item.objects.filter(user=request.user).delete()
