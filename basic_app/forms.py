from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo, Auction

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
            model = User
            fields = ('first_name','last_name','username','email','password')

class EditProfileForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('first_name','last_name','email',)

class AddAuctionForm(forms.ModelForm):
    class Meta():
        model = Auction
        exclude = ['author']
        widgets = {
            'due_date': forms.DateInput(attrs={'class':'datepicker'})
        }
    #    fields = ('title','description','picture','orig_price','bid_price','due_date')
