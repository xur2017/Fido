
from django import forms

class SendEmailForm(forms.Form):
    pet_id = forms.IntegerField(required=True, help_text="Message is sent to the users who favorited the pet.")
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
