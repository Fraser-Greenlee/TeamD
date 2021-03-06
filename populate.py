import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TeamD.settings')
import django
django.setup()
from stockedup.models import Item, Supplier
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# generate datetimes for lastUpdated values
def NdaysAgo(n):
	return datetime.now() - timedelta(days=n)

def populate():
	# clear tables
	Supplier.objects.all().delete()
	Item.objects.all().delete()
	# insert supplier values
	ss = []
	ss.append( Supplier(name='Bean Bros', email='B@mail.com') )
	ss.append( Supplier(name='He Bos', email='O@mail.com') )
	ss.append( Supplier(name='HJ Ohs', email='H@mail.com') )
	ss.append( Supplier(name='Af Hios', email='A@mail.com') )
	for s in ss:
		s.save()
	# insert item values, same for every current user
	for user in User.objects.all():
		Item(user=user, supplier=ss[0], name='Carrots',rate=5.0, cost=0.6, stock=13.5, lastUpdated=NdaysAgo(9)).save()
		Item(user=user, supplier=ss[2], name='Soup', 	rate=9.0, cost=0.9, stock=15.0, lastUpdated=NdaysAgo(3)).save()
		Item(user=user, supplier=ss[0], name='Steak', 	rate=15.0,cost=1.9, stock=23.0, lastUpdated=NdaysAgo(1)).save()

# Start execution here!
if __name__ == '__main__':
	print("Starting Rango population script...")
	populate()
