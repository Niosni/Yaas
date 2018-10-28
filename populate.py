import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','YAAS.settings')

import django
django.setup()

## FAKE POP SCRIPT
import random
from basic_app.models import Auction, UserProfileInfo
from faker import Faker
from django.contrib.auth.models import User

fakegen = Faker()
titles = ['Mug', 'Car', 'House', 'Bicycle', 'Television']
prices = [1,2.50,200,1000]

def add_User():
    u = User.objects.get_or_create(username=random.choice(topics))[0]
    t.save()
    return t

def populate(N=5):

    for entry in range(N):
        #get the topic for the entry
        tit = random.choice(topics)
        #Create fake data for that entry
        fake_desc = fakegen.company()
        fake_price = random.choice(prices)
        #Create the new Webpage
        Auction = Auction.objects.get_or_create(title=tit, description=fake_desc, price=fake_price)[0]


if __name__ == '__main__':
    print("populating script!")
    populate(20)
    print("pop complete")
