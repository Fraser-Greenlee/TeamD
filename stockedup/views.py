from django.shortcuts import render, redirect
from stockedup.models import Supplier, Item
import datetime

def index(request):
    return redirect('/accounts/login/')


def stock(request):
    currentUser = request.user
    items = filter(lambda x: x.user == currentUser, Item.objects.all())#Filters items to only the current user
    contextDict = {'stock': [], 'orders': []}
    datedOrders = {'Fri 26 Nov': [{'total': 26, 'orders': [{'name': 'Salad', 'from': 'Harry Farms', 'cost': 30, 'amount': 10}]}]}
    orders = []
    for item in items:
        contextDict['stock']+=[{'name':item.name,'from':item.supplier,'kgmo':1,'amount':item.stock,'ppkg':2}]
#        daysLasting = 0
#        while(currentStock>0):
#            daysLasting += 1
#            currentStock = currentStock - item.rate
        orders += [(int(item.stock/item.rate), item)]
    sorted(orders, key=lambda order: order[0]) #Sort by days lasting
    days = ("Mon","Tues","Wed","Thurs","Fri","Sat","Sun")
    months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    for order in orders:
        orderDate = datetime.date.today() + datetime.timedelta(order[0])
        stringDate = str(days[orderDate.weekday()]) + ' ' + str(orderDate.day) + ' ' + str(months[orderDate.month-1])
        datedOrders[stringDate] = datedOrders.get(stringDate,[]) + [{'total': datedOrders.get(stringDate,{}).get('total',0)+10, 'orders': datedOrders.get(stringDate,[]) + [{'name': order[1].name, 'from': order[1].supplier, 'cost': 30, 'amount': 10}]}]
    for day in datedOrders:
        for order in datedOrders[day]:
            contextDict['orders'] += [{'date': day, 'total': order['total'], 'orders': order['orders']}]
     # sample data
    print contextDict
    return render(request, 'stockedup/stock.html', context=contextDict)
