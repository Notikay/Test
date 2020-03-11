from django.contrib import admin
from django.urls import path
from product.views import *

app_name = "product"
urlpatterns = [
	path('show/', ResultListView.as_view({'get': 'list'})),
]