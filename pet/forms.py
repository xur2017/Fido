
from django import forms

class SendEmailForm(forms.Form):
    pet_id = forms.IntegerField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
