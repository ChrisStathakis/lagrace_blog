from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
	# name = forms.CharField(require=True, label='Ονοματεπώνυμο', widget=forms.CharInput({'class':'form-class'}))
    # subject = forms.CharField(require=True, label='Ονοματεπώνυμο', widget=forms.CharInput({'class':'form-class'}))
    # email = forms.EmailField(require=True, label='Ονοματεπώνυμο', widget=forms.CharInput({'class':'form-class'}))

    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['is_readed', ]