from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView

from ApartmentsApp.forms import ApartmentsFormSet, AddressInlineFormSet, RoomInlineFormSet
from ApartmentsApp.models import Apartments, Address


class ApartmentsPage(TemplateView):
    template_name = 'ApartmentsApp/Apartments.html'

    def get(self, request, *args, **kwargs):
        apartments = Apartments.objects.order_by('name')
        address = Apartments.objects.get(id=kwargs['pk'])
        response = {
            'form_set': ApartmentsFormSet(queryset=apartments),
            'address_inline_formset': AddressInlineFormSet(instance=address),
            'room_inline_formset': RoomInlineFormSet(instance=address),
        }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        formset = ApartmentsFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            # do something.
        else:
            print('! Form Validation Error')
            formset.add_error(field=None, error='Form Validation Error')
        return redirect(to='main-page')


class ApartmentsList(ListView):
    template_name = 'ApartmentsApp/apartment_list.html'
    model = Apartments
