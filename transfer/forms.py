from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder, Field
from django import forms
from django.core.exceptions import ValidationError


class TransferForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=20, decimal_places=2, required=True, validators=[])

    def __init__(self, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.field_class = 'col-lg-4'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('amount', placeholder='Amount to transfer'),
            ButtonHolder(Submit('submit', 'Transfer', css_class='btn-primary'))
        )

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if data <= 0:
            raise ValidationError("Amount must be greater then 0!")

        return data

    class Meta:
        fields = '__all__'
