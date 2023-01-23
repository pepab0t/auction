from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import NewListingForm
from .models import Listing, User


def index(request):
    items = Listing.objects.all()

    return render(request, "auctions/index.html", {"items": items})


@login_required
def new_item(request):
    if request.method == "POST":
        # title = request.POST["title"]
        # desc = request.POST["desc"]
        # bid = request.POST["bid"]
        # cat = request.POST["cat"]

        # if "myimage" in request.FILES:
        #     image = request.FILES["myimage"]
        # else:
        #     image = None

        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            if "image" in request.FILES:
                listing.image = request.FILES["image"].file.read()
            listing.user = request.user
            listing.save()
            print("saved")
        else:
            print(form.errors)

        return HttpResponseRedirect(reverse("index"))

    else:
        form = NewListingForm()
    return render(
        request,
        "auctions/new_listing.html",
        {"categories": Listing.CATEGORIES, "form": form},
    )


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
            user = User.objects.create_user(username, email, password)
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
