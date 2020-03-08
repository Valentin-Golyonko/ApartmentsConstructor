from django import forms
from django.forms import modelformset_factory, inlineformset_factory

from ApartmentsApp.models import (Apartments, Chair, Room)


class ApartmentsForm(forms.ModelForm):
    prefix = 'apartments'

    class Meta:
        model = Apartments
        fields = ('name', 'country', 'city', 'street',)


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('count', 'squire_size',)


class ChairForm(forms.ModelForm):
    class Meta:
        model = Chair
        fields = ('amount',)


RoomFormset = modelformset_factory(Room, form=RoomForm, fields=('count', 'squire_size',),
                                   extra=0, can_delete=True, )
ChairFormset = modelformset_factory(Chair, form=ChairForm, fields=('amount',),
                                    extra=0, can_delete=True, )

ChairInlineFormset = inlineformset_factory(parent_model=Room, model=Chair, form=ChairForm, fields=('amount',),
                                           # formset=ChairFormset,
                                           extra=0, can_delete=True, )
