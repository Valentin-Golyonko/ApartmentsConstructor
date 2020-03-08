from django.contrib import admin
from django.urls import path, include

from ApartmentsApp.views import (ApartmentsList, ApartmentsPageDetails, AddApartments)

app_name = 'apartments'

urlpatterns = [
    path('', ApartmentsList.as_view(), name='list'),
    path('details/<int:pk>/', ApartmentsPageDetails.as_view(), name='details'),
    path('add/', AddApartments.as_view(), name='add'),
]
