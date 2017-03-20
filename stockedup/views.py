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
        print(datedOrders.get(stringDate, 0))
        datedOrders[stringDate] = {'total': datedOrders.get(stringDate, {'total': 0})['total'] + 10,
                                   'orders': datedOrders.get(stringDate, {'orders': []})['orders'] + [
                                       {'name': order[1].name,
                                        'from': order[1].supplier,
                                        'cost': 30, 'amount': 10}]}

        #            datedOrders.get(stringDate,{}) + \
        #                                 {'total': 10,
        #                                   'orders': datedOrders.get(stringDate,[]) + [{'name': order[1].name,
        #                                                                                'from': order[1].supplier,
        #                                                                                'cost': 30, 'amount': 10}]}
        print(datedOrders[stringDate])
    for day in datedOrders:
        tempList = []
        for order in datedOrders[day]['orders']:
            tempList += [order]
        contextDict['orders'] += [{'date': day, 'total': datedOrders[day]['total'], 'orders': tempList}]


            # sample data
    print contextDict
    return render(request, 'stockedup/stock.html', context=contextDict)
