
from django import forms
from .models import CustomUser, Pet

class CreateUserForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        template_name = 'user/user_form.html'
        model = CustomUser
        fields = ['user_type', 'first_name', 'last_name', 'email', 'username', 'password', 'password_confirm', 'phone_number',
                  'street_number', 'street_name', 'city', 'state', 'zip']
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(),
            #'profilePic' : forms.FileInput()
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        #self.fields['profilePic'].label = "Profile Picture"

    def clean(self):
        super(CreateUserForm, self).clean()
        error_message = ''
        field = ''
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirm'):
            error_message = 'Passwords do not match.'
            field = 'password'
            self.add_error(field, error_message)
            raise forms.ValidationError(error_message)
        return self.cleaned_data

class SendEmailForm(forms.Form):
    pet_id = forms.IntegerField(required=True, help_text="Message is sent to the users who favorited the pet.")
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self,*args,**kwargs):
        self.user_id = kwargs.pop('user_id')
        super(SendEmailForm, self).__init__(*args,**kwargs)
        self.fields['pet_id'].widget = forms.Select( choices = Pet.objects.filter(users__pk = self.user_id).values_list('id', 'name') )
