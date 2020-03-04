from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView

from ApartmentsApp.forms import ApartmentsFormSet, AddressInlineFormSet, RoomInlineFormSet, ApartmentsForm
from ApartmentsApp.models import Apartments


class ApartmentsPage(TemplateView):
    template_name = 'ApartmentsApp/Apartments.html'

    def get(self, request, *args, **kwargs):
        apartment = Apartments.objects.get(pk=kwargs['pk'])
        response = {
            'apartment_form': ApartmentsForm(instance=apartment),
            'address_inline_formset': AddressInlineFormSet(instance=apartment),
            'room_inline_formset': RoomInlineFormSet(instance=apartment),
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


class ApartmentsList(ListView):
    template_name = 'ApartmentsApp/apartment_list.html'
    model = Apartments
