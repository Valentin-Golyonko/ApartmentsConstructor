from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin

from ApartmentsApp.forms import AddressInlineFormset, RoomInlineFormset, ApartmentsForm, \
    ApartmentsRoomsWithChairsFormset
from ApartmentsApp.models import Apartments


class ApartmentsList(ListView):
    template_name = 'ApartmentsApp/apartment_list.html'
    model = Apartments


class ApartmentsPageDetailsOld(TemplateView):
    """--------------- 1 nested FK ---------------"""
    template_name = 'ApartmentsApp/apartments_details_old.html'

    def get(self, request, *args, **kwargs):
        apartment = Apartments.objects.get(pk=kwargs['pk'])
        response = {
            'apartment_form': ApartmentsForm(instance=apartment),
            'address_inline_formset': AddressInlineFormset(instance=apartment),
            'room_inline_formset': RoomInlineFormset(instance=apartment),
        }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request, *args, **kwargs):
        apartment = Apartments.objects.get(pk=kwargs['pk'])
        apartment_form = ApartmentsForm(request.POST, instance=apartment)
        if apartment_form.is_valid():
            apartment_form.save()
            # do something.
        else:
            print('! Form Validation Error')
            apartment_form.add_error(field=None, error='Form Validation Error')
        return redirect(to='list')


class ApartmentsPageDetails(SingleObjectMixin, FormView):
    model = Apartments
    template_name = 'ApartmentsApp/apartments_details.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Apartments.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Apartments.objects.all())
        return super().get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return ApartmentsRoomsWithChairsFormset(**self.get_form_kwargs(),
                                                instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(self.request,
                             messages.SUCCESS,
                             'Changes were saved.')

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('list')
