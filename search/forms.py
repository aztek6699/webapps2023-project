from crispy_forms.helper import FormHelper
from django import forms


class SearchForm(forms.Form):
    email = forms.EmailField(label='Email', required=False, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    name = forms.CharField(label='Name', required=False, widget=forms.TextInput(attrs={'placeholder': 'Name'}))

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_show_labels = False

    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if not data and self.is_bound:
    #         raise forms.ValidationError('Fill one please')
    #     return data
    #
    # def clean_name(self):
    #     data = self.cleaned_data['name']
    #     if not data and self.is_bound:
    #         raise forms.ValidationError('Fill one please')
    #     return data

    class Meta:
        fields = '__all__'
