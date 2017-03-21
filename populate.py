import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TeamD.settings')
import django
django.setup()
from stockedup.models import Item, Supplier
from django.contrib.auth.models import User
from datetime import datetime

def populate():
	# clear tables
	Supplier.objects.all().delete()
	Item.objects.all().delete()
	# insert values
	ss = []
	ss.append( Supplier(name='Bean Bros', email='B@mail.com') )
	ss.append( Supplier(name='He Bos', email='O@mail.com') )
	ss.append( Supplier(name='HJ Ohs', email='H@mail.com') )
	ss.append( Supplier(name='Af Hios', email='A@mail.com') )
	for s in ss:
		s.save()
	#
	Item(user=User.objects.all()[0], supplier=ss[0], name='Carrots',rate='5', cost=0.6, stock=13.5, lastUpdated=datetime.now()).save()
	Item(user=User.objects.all()[0], supplier=ss[1], name='Beans', 	rate='3', cost=0.1, stock=9.0, 	lastUpdated=datetime.now()).save()
	Item(user=User.objects.all()[0], supplier=ss[2], name='Soup', 	rate='9', cost=0.9, stock=15.0, lastUpdated=datetime.now()).save()
	Item(user=User.objects.all()[0], supplier=ss[0], name='Steak', 	rate='15',cost=1.9, stock=23.0, lastUpdated=datetime.now()).save()

# Start execution here!
if __name__ == '__main__':
	print("Starting Rango population script...")
	populate()
