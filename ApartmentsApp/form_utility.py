from ApartmentsApp.forms import (ApartmentsForm, ChairForm)


class FormsList:
    apartments_form = ApartmentsForm()

    def __init__(self, queryset):
        self.form_data = queryset

        self.forms = {
            'apartments': ApartmentsForm(),
            'chair': ChairForm(),
        }

    def get_form(self, form_name: str):
        return self.forms.get(form_name, None)
