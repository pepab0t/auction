import re
from typing import Optional

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.defaulttags import register
from django.urls import reverse

from .forms import NewListingForm
from .models import Bid, Comment, Listing, User, Wishlist


@register.filter
def active_wishlist(wishlist, status):
    return Listing.objects.filter(id__in=wishlist.values("listing_id"), active=status)

@register.filter
def nothing(thing):
    return thing

def index(request):
    items = Listing.objects.filter(active=True)

    if "messages" not in request.session:
        request.session["messages"] = []

    return render(request, "auctions/index.html", {"title": "Active Listings", "items": items})

def category_filter(request, category: Optional[str]):
    if category == "None":
        category = None
    
    items = Listing.objects.filter(category=category, active=True)
    item_first = items.first()
    if not items.exists() or item_first is None:
        return render(request, "auctions/error.html", {
            "title": f"Invalid category '{category}'"
        })

    return render(request, "auctions/index.html", {"title": f"Category: {item_first.get_category_display()}", "items": items})

@login_required
def wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    listings = Listing.objects.filter(id__in=wishlist.values("listing_id"), active=True)

    return render(request, "auctions/index.html", {"title": "My Wishlist", "items": listings})

@login_required
def my_wins(request):

    listings = request.user.wins.all()

    return render(request, "auctions/index.html", {"title": "My Wins", "items": listings})

@login_required
def my_auctions(request):
    listings = Listing.objects.filter(user=request.user)

    return render(request, "auctions/index.html", {
        "title": "My Auctions",
        "items": listings
    })

@login_required
def comment(request, listing_id: int):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)

        text = request.POST["comment"]
        c = Comment(listing=listing, text=text, user=request.user)
        c.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))

@login_required
def delete_comment(request, comment_id: int):
    comment = Comment.objects.get(pk=comment_id)

    if request.user == comment.user:
        comment.delete()
        
    return HttpResponseRedirect(reverse('listing', kwargs={"listing_id": comment.listing.id}))


@login_required
def new_item(request):
    if request.method == "POST":

        listing = NewListingForm(request.POST, request.FILES)
        if listing.is_valid():

            bid_val = request.POST["bid"]
            try:
                bid_float = float(bid_val)
            except ValueError:
                return render(request, "auctions/new_listing.html", {
                    "form": listing,
                    "messages": ["Bid must be a number format"]
                })

            if bid_float <= 0:
                return render(request, "auctions/new_listing.html", {
                    "form": listing,
                    "messages": ["Starting bid must be grater than zero!"]
                })



            listing = listing.save(commit=False)
            listing.user = request.user
            listing.save()

            # listing = Listing.objects.get(pk=listing.id)

            bid = Bid.objects.create(value = bid_val, user = request.user, listing=listing)

            print("saved")
        else:
            print(listing.errors)

        return HttpResponseRedirect(reverse("index"))

    else:
        listing = NewListingForm()
    return render(
        request,
        "auctions/new_listing.html",
        {"form": listing},
    )

def listing(request, listing_id: int):
    listing = Listing.objects.get(pk=listing_id)

    user = request.user
    if isinstance(user, AnonymousUser):
        wishlist = None 
    else:
        wishlist = Wishlist.objects.filter(user=user, listing=listing).first()

    max_bid = listing.bids.order_by('-value').first()

    messages = request.session["messages"].copy()
    request.session['messages'] = []

    return render(request, "auctions/listing.html", {
        "listing": listing, 
        "wishlist": wishlist,
        "max_bid": max_bid, 
        "author": listing.user,
        "messages": messages
    })

@login_required
def bid(request, listing_id: int):
    kwargs = {
        "listing_id": listing_id,
    }
    if request.method == "POST":
        try:
            new_bid = float(request.POST['bid'])
        except ValueError:
            request.session['messages'] += ["Bid must be number"]
            print(request.session['messages'])
            return HttpResponseRedirect(reverse('listing', kwargs=kwargs))

        listing = Listing.objects.get(pk=listing_id)
        current_bid = listing.bids.order_by("-value").first()
        if new_bid < current_bid.value:
            request.session['messages'] += [f"Bid must be greater than current bid: ${current_bid.value}"]
            return HttpResponseRedirect(reverse('listing', kwargs=kwargs))

        Bid.objects.create(value=new_bid, listing=listing, user=request.user)
        print(f"bid saved {new_bid}")

    return HttpResponseRedirect(reverse("listing", kwargs=kwargs))

@login_required
def mark_wishlist(request, listing_id: int):
    # add to wishlist
    listing = Listing.objects.get(pk=listing_id)

    wishlist = Wishlist.objects.filter(user=request.user, listing=listing)

    if wishlist.exists():
        wishlist.delete()
    else:
        wishlist = Wishlist(user=request.user, listing=listing)
        wishlist.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))

@login_required
def close(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    winner_bid = listing.bids.order_by("-value").first()
    
    if winner_bid is None:
        listing.close()
    if winner_bid.user == listing.user:
        listing.close()
    else:
        listing.close(winner_bid.user)

    return HttpResponseRedirect(reverse('listing', kwargs={"listing_id": listing_id}))


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)# type: ignore
            user.save()

        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
