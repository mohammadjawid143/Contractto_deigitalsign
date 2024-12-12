# forms.py
from django import forms
import datetime

from django import forms
from .models import Contract

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['full_name', 'recipient_email', 'contract_text']

    def save(self, commit=True):
        contract = super().save(commit=False)
        contract.contract_text = contract.contract_text or (
            "This is a sample contract.\n\n"
            "Full Name: _____________\n"
            "Date: _____________\n"
            "Signature: _____________"
        )
        if commit:
            contract.save()
        return contract



# class ContractForm(forms.Form):
#     recipient_email = forms.EmailField(label="Recipient Email")
#     full_name = forms.CharField(label="Full Name of Recipient")
#     contract_text = forms.CharField(
#         widget=forms.Textarea(attrs={'placeholder': 'Lorem Ipsum...'}),
#         initial="Lorem Ipsum..."
#     )
#     date = forms.DateField(initial=datetime.date.today)
