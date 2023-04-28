from base.models import CURRENCY_CHOICES
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, ButtonHolder, Row, Column
from django import forms


class ChangeCurrencyForm(forms.Form):
    currency = forms.CharField(max_length=3, widget=forms.Select(choices=CURRENCY_CHOICES))

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.field_class = 'col-lg-4'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column(HTML('<p>Currency:</p>'), css_class='form-group col-md-1 mb-0'),
                Column('currency', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(Submit('submit', 'Update Currency', css_class='btn-primary'),)
        )
