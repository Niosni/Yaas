from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo, Auction


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = UserProfileInfo
        fields = ('language',)


class EditProfileForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email',)


class AddAuctionForm(forms.ModelForm):
    class Meta():
        model = Auction
        exclude = ('author', 'bidder', 'state')
        widgets = {
            'due_date': forms.DateInput(attrs={'class': 'datepicker'})
        }
    #    fields = ('title','description','picture','orig_price','bid_price','due_date')


class EditAuctionForm(forms.ModelForm):
    class Meta():
        model = Auction
        fields = ('description',)


class SearchAuctionsForm(forms.ModelForm):
    class Meta():
        model = Auction
        fields = ('title',)
