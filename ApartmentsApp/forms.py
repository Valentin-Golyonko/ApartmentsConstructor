from django import forms
from django.forms import modelformset_factory, inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _

from ApartmentsApp.models import Apartments, Address, Room, Chair
from ApartmentsApp.utils import is_empty_form, is_form_persisted


class ApartmentsForm(forms.ModelForm):
    class Meta:
        model = Apartments
        fields = "__all__"


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"


class ChairForm(forms.ModelForm):
    class Meta:
        model = Chair
        fields = "__all__"


ApartmentsFormset = modelformset_factory(Apartments, form=ApartmentsForm, fields='__all__',
                                         extra=1, )

AddressInlineFormset = inlineformset_factory(parent_model=Apartments, model=Address, fields='__all__',
                                             extra=1, )
RoomInlineFormset = inlineformset_factory(parent_model=Apartments, model=Room, fields='__all__',
                                          extra=1, )
ChairInlineFormset = inlineformset_factory(parent_model=Room, model=Chair, fields='__all__',
                                           extra=1, )


class BaseRoomWithChairFormset(BaseInlineFormSet):
    """
    The base formset for editing Rooms belonging to a Apartments, and the
    Chairs belonging to those Rooms.
    """

    def add_fields(self, form, index):
        super().add_fields(form, index)

        # Save the formset for a Chair's in the nested property.
        form.nested = ChairInlineFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            prefix='chair-%s-%s' % (form.prefix, ChairInlineFormset.get_default_prefix()),
        )

    def is_valid(self):
        """ Also validate the nested formsets. """
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()
        return result

    def clean(self):
        """
        If a parent form has no data, but its nested forms do, we should
        return an error, because we can't save the parent.
        For example, if the Room form is empty, but there are Chair.
        """
        super().clean()

        for form in self.forms:
            if not hasattr(form, 'nested') or self._should_delete_form(form):
                continue
            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_('You are trying to add chair(s) to a room which '
                            'does not yet exist. Please add information '
                            'about the room and edit chair again.'))

    def save(self, commit=True):
        """ Also save the nested formsets. """
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)
        return result

    def _is_adding_nested_inlines_to_empty_form(self, form):
        """
        Are we trying to add data in nested inlines to a form that has no data?
        e.g. Adding Chairs to a new Room whose data we haven't entered?
        """
        if not hasattr(form, 'nested'):
            # A basic form; it has no nested forms to check.
            return False
        if is_form_persisted(form):
            # We're editing (not adding) an existing model.
            return False

        if not is_empty_form(form):
            # The form has errors, or it contains valid data.
            return False

        # All the inline forms that aren't being deleted:
        non_deleted_forms = set(form.nested.forms).difference(
            set(form.nested.deleted_forms)
        )

        # At this point we know that the "form" is empty.
        # In all the inline forms that aren't being deleted, are there any that
        # contain data? Return True if so.
        return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)


# This is the formset for the Rooms belonging to a Apartments and the
# Chairs belonging to those Rooms.
#
# You'd use this by passing in a Publisher:
#       ApartmentsRoomsWithChairsFormset(**form_kwargs, instance=self.object)
ApartmentsRoomsWithChairsFormset = inlineformset_factory(
    parent_model=Apartments,
    model=Room,
    formset=BaseRoomWithChairFormset,
    fields="__all__",
    extra=1,
)
