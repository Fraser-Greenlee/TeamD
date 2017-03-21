from django.conf.urls import url, include
from django.contrib import admin
from stockedup import views
from registration.backends.simple.views import RegistrationView

#Create a new class that redirects the user to the stock page,
#if successful at logging
class MyRegistrationView(RegistrationView):
	def get_success_url(self, user):
		return '/stock/'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^stock', views.stock, name='stock'),
	url(r'^ajax/save', views.save, name='save'),
  url(r'^admin/', admin.site.urls),
	url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
]
