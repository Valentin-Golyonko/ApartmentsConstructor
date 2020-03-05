from django import forms
from django.forms import modelformset_factory, inlineformset_factory

from ApartmentsApp.models import Apartments, Address, Room


class ApartmentsForm(forms.ModelForm):
    class Meta:
        model = Apartments
        fields = "__all__"


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"


ApartmentsFormSet = modelformset_factory(Apartments, form=ApartmentsForm, fields='__all__',
                                         extra=0, )

AddressInlineFormSet = inlineformset_factory(parent_model=Apartments, model=Address, fields='__all__',
                                             extra=0, )
RoomInlineFormSet = inlineformset_factory(parent_model=Apartments, model=Room, fields='__all__',
                                          extra=0, )
