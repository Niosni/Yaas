from django.shortcuts import render, redirect
from basic_app.forms import UserForm, EditProfileForm, AddAuctionForm, EditAuctionForm, SearchAuctionsForm
from basic_app.models import Auction
from basic_app.models import User
# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import urllib.request

import requests
import json
API_URL = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey=N5W66DMTP80L3027"


def index(request):
    return render(request, 'basic_app/index.html')


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.language = 'en'
            user.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'basic_app/registration.html',
                  {'user_form': user_form,
                   'registered': registered})


def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            # Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # Nothing has been provided for username or password.
        return render(request, 'basic_app/login.html', {})


@login_required
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'basic_app/profile.html', args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        # First get the username and password supplied
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return render(request, 'basic_app/profile.html')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'basic_app/edit_profile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        # First get the username and password supplied
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            uusjuttu = form.save()
            update_session_auth_hash(request, uusjuttu.user)
            return render(request, 'basic_app/profile.html')
        else:
            print("Not successful pw change")
            return render(request, 'basic_app/profile.html')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'basic_app/change_password.html', args)


def auctions(request):
    auctions_list = Auction.objects.order_by('title').filter(state='Active')
    searchForm = SearchAuctionsForm()
    currency = "€"
    auct_dict = {'auctions': auctions_list,
                 'searchForm': searchForm,
                 'currency': currency}
    return render(request, 'basic_app/auctions.html', context=auct_dict)


def add_auction(request):
    if request.method == 'POST':
        form = AddAuctionForm(request.POST)
        if form.is_valid():
            a = Auction(author=request.user,
                        title=request.POST['title'],
                        description=request.POST['description'],
                        due_date=request.POST['due_date'],
                        price=request.POST['price'],
                        state='Active',
                        )
            a.save()
            print('WORKING')
            return redirect('basic_app:auctions')
        else:
            print('NOT WORKING')

    else:
        print(request.user)

        form = AddAuctionForm(request.POST)
        # form.clean_author()
        return render(request, 'basic_app/add_auction.html', {'aaf': form})


def save_bid(request):
    if request.method == 'POST':
        id = request.POST['id']
        a = Auction.objects.get(id=id)
        old_bidder_email = ""
        if a.bidder:
            old_bidder_name = a.bidder
            old_bidder_email = User.objects.get(username=old_bidder_name).email

        a.price = request.POST['bid_price']
        a.bidder = request.user.username
        a.save()
        notify_bid(a, old_bidder_email)
        return redirect('basic_app:auctions')


def ban_auction(request):
    if request.method == 'POST':
        id = request.POST['auction_id']
        a = Auction.objects.get(id=id)
        if a.state == 'Banned':
            a.state = 'Active'
        else:
            a.state = 'Banned'
            author = User.objects.get(username=a.author).email
            if a.bidder:
                bidder = User.objects.get(username=a.bidder).email
            else:
                bidder = ''
            send_mail(
                'Auction has been banned',
                'Against our terms',
                'no-reply@yet-another-auction-site.com',
                [author, bidder]
            )
        a.save()
    return redirect('basic_app:auctions')


def notify_bid(auction, old_bidder):
    seller = auction.author
    if auction.bidder != old_bidder:
        send_mail(
            'Someone bid higher than you!',
            'Someone has bid higher you in ' + auction.title,
            'no-reply@yet-another-auction-site.com',
            [old_bidder],
            fail_silently=False,
        )
    send_mail(
        'Your item has a new bid!',
        'Your item ' + auction.title + 'has a new bid of ' + auction.price,
        'no-reply@yet-another-auction-site.com',
        [seller],
        fail_silently=False,
    )


def confirm_bid(request):

    if request.method == 'POST':
        id = request.POST['id']
        bid_price = request.POST['bid_price']
        auction = Auction.objects.get(id=id)
        auct_dict = {'auction': auction, 'bid_price': bid_price}
        return render(request, 'basic_app/confirm_bid.html', context=auct_dict)


def make_bid(request):

    if request.method == 'POST':
        id = request.POST['auction_id']
        auction = Auction.objects.get(id=id)
        print(auction.price)
        # Minimum of 1 cent of bidding
        auction.price = round((float(str(auction.price)) + float(0.01)), 2)
        auct_dict = {'auction': auction}
        # return render(request, 'basic_app/auctions.html', context=auct_dict)

        return render(request, 'basic_app/make_bid.html', context=auct_dict)


def edit_auction(request, id):

    print(id, 'testi')

    if request.method == 'GET':
        a = Auction.objects.get(id=id)
        return render(request, 'basic_app/edit_auction.html', {'description': a.description})

    if request.method == 'POST':
        a = Auction.objects.get(id=id)
        print(a.description)
        a.description = request.POST['description']
        a.save()
        all_auctions = Auction.objects.all()
        args = {
            'message': 'Auction ' + str(id) + " desc edited",
            'auctions': all_auctions
        }
        return render(request, 'basic_app/auctions.html', args)


def searchAuctions(request):
    title = request.POST['title']
    print(title)
    if request.method == 'POST':
        results = Auction.objects.filter(title__contains=title)
        print(results)
        return render(request, 'basic_app/auctions.html', {'auctions': results})


def show_banned(request):
    if request.user.is_superuser:
        banned = Auction.objects.filter(state='Banned')
        return render(request, 'basic_app/auctions.html', {'auctions': banned})
    else:
        return redirect('basic_app:auctions')


def change_currency(request):
    response = requests.get(API_URL).json()

    eur_to_usd = response['Realtime Currency Exchange Rate']['5. Exchange Rate']

    print(eur_to_usd)

    auctions_list = Auction.objects.order_by('title').filter(state='Active')

    for auction in auctions_list:
        auction.price = float(auction.price) * float(eur_to_usd)

    searchForm = SearchAuctionsForm()
    currency = "$"
    auct_dict = {'auctions': auctions_list,
                 'searchForm': searchForm,
                 'currency': currency}

    return render(request, 'basic_app/auctions.html', context=auct_dict)
