from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from ApartmentsApp.forms import (ApartmentsForm, RoomFormset, ChairFormset, ChairInlineFormset)
from ApartmentsApp.models import (Apartments, Room, Chair)


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
        room = Room.objects.filter(apartment_id=kwargs['pk']).first()
        response = {
            'messages': get_messages(request),
            'apartment_form': ApartmentsForm(instance=apartment),
            'room_formset': RoomFormset(queryset=rooms, prefix='room'),
            'chair_formset': ChairInlineFormset(instance=room, prefix='chair'),
        }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request, *args, **kwargs):
        print("POST:", request.POST)
        apartment = Apartments.objects.get(pk=kwargs['pk'])
        rooms = Room.objects.filter(apartment_id=kwargs['pk'])
        room = Room.objects.filter(apartment_id=kwargs['pk']).first()

        apartment_form = ApartmentsForm(request.POST, instance=apartment)
        room_formset = RoomFormset(request.POST, queryset=rooms, prefix='room')
        chair_formset = ChairInlineFormset(request.POST, instance=room, prefix='chair')

        if apartment_form.is_valid() and room_formset.is_valid() and chair_formset.is_valid():
            apartment_form.save()
            room_formset.save()
            chair_formset.save()
            messages.success(request, 'Apartments saved.')
        else:
            messages.error(request, 'Form Validation Error.')
            apartment_form.add_error(field=None, error='Form Validation Error')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('apartments:list')


class AddApartments(TemplateView):
    template_name = 'ApartmentsApp/add.html'

    def get(self, request, *args, **kwargs):
        response = {

        }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('apartments:list')
