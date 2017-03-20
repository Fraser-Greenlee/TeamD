from django.shortcuts import render, redirect
from stockedup.models import Supplier, Item
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
        contextDict['stock'] += [{'name': item.name, 'from': item.supplier, 'kgmo': 1, 'amount': item.stock, 'ppkg': 2}]
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
