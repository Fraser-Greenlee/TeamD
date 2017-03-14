from django.contrib import admin
from stockedup.models import Supplier, User, Item
# Register your models here.
admin.site.register(Supplier)
admin.site.register(Item)