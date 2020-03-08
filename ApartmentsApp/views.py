from django.contrib import messages
from django.contrib.messages import get_messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView

from ApartmentsApp.forms import *
from ApartmentsApp.models import Apartments


class ApartmentsList(ListView):
    template_name = 'ApartmentsApp/apartment_list.html'
    model = Apartments

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response['messages'] = get_messages(request)
        return response


class ApartmentsPageDetails(TemplateView):
    template_name = 'ApartmentsApp/apartments_details.html'

    def get(self, request, *args, **kwargs):
        apartment = Apartments.objects.get(pk=kwargs['pk'])
        rooms = Room.objects.filter(apartment_id=kwargs['pk'])
        chairs = Chair.objects.filter(room__apartment_id=kwargs['pk'])
        response = {
            'messages': get_messages(request),
            'apartment_form': ApartmentsForm(instance=apartment),
            'room_formset': RoomFormset(queryset=rooms),
            'chair_formset': ChairFormset(queryset=chairs),
        }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request, *args, **kwargs):
        print("POST:", request.POST)
        apartment = Apartments.objects.get(pk=kwargs['pk'])
        rooms = Room.objects.filter(apartment_id=kwargs['pk'])
        chairs = Chair.objects.filter(room__apartment_id=kwargs['pk'])

        apartment_form = ApartmentsForm(request.POST, instance=apartment)
        room_formset = RoomFormset(request.POST, queryset=rooms)
        chair_formset = ChairFormset(request.POST, queryset=chairs)

        if apartment_form.is_valid() and room_formset.is_valid() and chair_formset.is_valid():
            apartment_form.save()
            room_formset.save()
            chair_formset.save()
            messages.success(request, 'Apartments saved.')
        else:
            messages.error(request, 'Form Validation Error.')
            apartment_form.add_error(field=None, error='Form Validation Error')
        return redirect(to='list')
