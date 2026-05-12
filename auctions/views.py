from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *



# update main page to reflect new bids


def index(request):
    active_listings = Listings.objects.filter(active=True)    
    return render(request, "auctions/index.html",{
        "flag": "ACTIVE",
        "active_listings": active_listings
    } )


# delete the old way and keep this way
def inactive_listings(request):
    listings_closed = Listings.objects.filter(active=False)
    return render(request, "auctions/index.html",{
        "flag": "INACTIVE",
        "active_listings":listings_closed
    })
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html")
    
    elif request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = int(request.POST["bid"])
        category = request.POST["category"]
        image_url = request.POST["image_url"]
        owner = request.user
        active = True

        new_listing = Listings(
            title = title,
            description = description,
            starting_price = bid,
            category = category,
            photo = image_url,
            owner = owner,
            active = active
        )
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))

def listing_page(request, id, message="Detail"):        #default message
    specific_listing = Listings.objects.get(id=id)
    title = specific_listing.title
    description = specific_listing.description
    price = specific_listing.starting_price
    photo = specific_listing.photo
    id = specific_listing.id
    active = specific_listing.active
    owner = specific_listing.owner
    selected_bids = Bid.objects.filter(item=specific_listing) 
    selected_comments = Comment.objects.filter(item=specific_listing)

    try:
        watchlist_items = Watchlist.objects.filter(user=request.user)

    except:
        watchlist_items = []

    watchlist = []
    for items in watchlist_items:
        post = items.item.id
        watchlist.append(post)


    # specific listing returns MonaLisa

    print("@@@@@@@@@@@@@@@@", watchlist)

    try:
        last_bid = selected_bids.last()
        last_bid_amount = last_bid.amount
        last_bid_user = last_bid.user
    except AttributeError:
        last_bid_amount = "No Current Bids"
        last_bid_user = "No Current Bids"

    return render(request, 'auctions/listing_page.html', {
        "title":title,
        "description":description,
        "starting_price":price,
        "photo":photo,
        "message":message,
        "id":id,
        "last_bid_amount":last_bid_amount,
        "selected_comments":selected_comments,
        "owner":owner,
        "active":active,
        "last_bid_user":last_bid_user,
        "watchlist_items": watchlist_items,
        "watchlist": watchlist
        }) 

def add_bid(request):
    if request.method == "POST":
        id = request.POST['id']
        new_bid = int(request.POST["new_bid"])
        item = Listings.objects.get(id=id)
        starting_price = item.starting_price
        selected_bids = Bid.objects.filter(item=item)
        last_bid = selected_bids.last()
        try:
            last_bid_amount = last_bid.amount
        except AttributeError:
            last_bid_amount = 0       

        if new_bid <= starting_price or new_bid <= last_bid_amount:
            #redirect user to same page with error message
            return HttpResponseRedirect(reverse("listing_page", args=[item.id, "Failure"]))
        else:
            current_bid = Bid(user=request.user, amount=new_bid, item=item)
            current_bid.save()
            return HttpResponseRedirect(reverse("listing_page", args=[item.id, "Success"]))
        


def category(request):
    if request.method == "POST":
        choose_category = request.POST["choose_category"]
        filtered_rows = Listings.objects.filter(category=choose_category)
        return render(request, 'auctions/category.html', {
            "filtered_rows":filtered_rows,
            "request": "POST"
        })
    else:
        return render(request, 'auctions/category.html')
    
def add_comment(request):
    if request.method == "POST":
        new_comment = request.POST["comment"]
        id = request.POST['id']
        item = Listings.objects.get(id=id)
        new_row = Comment(comment=new_comment, user=request.user, item=item)
        new_row.save()
        return HttpResponseRedirect(reverse("listing_page", args=[item.id, "Detail"]))
    

# The owner should be able to see the button (is authenticated)

def close_listing (request, id):
    listing = Listings.objects.get(id=id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing_page", args=[id, "Detail"]))

def watchlist_page(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist_page.html', {
        "watchlist_items": watchlist_items
    })

def add_watchlist(request):
    if request.method == "POST":
        id = request.POST['id']
        item = Listings.objects.get(id=id)
        user = request.user
        new_watchlist = Watchlist(item=item, user=user)
        new_watchlist.save()
        return HttpResponseRedirect(reverse("listing_page", args=[id, "Detail"]))
    
def delete_watchlist(request):
    if request.method == "POST":
        id = request.POST['id']
        item = Listings.objects.get(id=id)
        user = request.user
        delete_watchlist_row = Watchlist.objects.get(item=item, user=user)
        delete_watchlist_row.delete()
        return HttpResponseRedirect(reverse("listing_page", args=[id, "Detail"]))
