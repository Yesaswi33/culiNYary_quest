from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Recepie


@login_required
def receipes(request):
    if request.method == "POST":
        # Search Form
        if "search" in request.POST:
            search_query = request.POST.get("search")
            receipes = Recepie.objects.filter(receipe_name__icontains=search_query, user=request.user)
        else:
            # Add Recipe Form
            name = request.POST.get("receipe_name")
            desc = request.POST.get("receipe_description")
            price = request.POST.get("receipe_price") or 0
            image = request.FILES.get("receipe_image")

            Recepie.objects.create(
                user=request.user,
                receipe_name=name,
                receipe_description=desc,
                receipe_price=price,
                receipe_image=image
            )
            return redirect("receipes")
    else:
        receipes = Recepie.objects.filter(user=request.user)

    return render(request, "receipes.html", {"receipes": receipes})


@login_required
def delete_receipe(request, id):
    receipe = Recepie.objects.get(id=id)
    receipe.delete()
    return redirect("receipes")


@login_required
def update_receipe(request, id):
    receipe = Recepie.objects.get(id=id)

    if request.method == "POST":
        receipe.receipe_name = request.POST.get("receipe_name")
        receipe.receipe_description = request.POST.get("receipe_description")
        receipe.receipe_price = request.POST.get("receipe_price") or 0

        if request.FILES.get("receipe_image"):
            receipe.receipe_image = request.FILES.get("receipe_image")

        receipe.save()
        return redirect("receipes")

    return render(request, "update_receipes.html", {"receipes": receipe})


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid username!")
            return redirect("login")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid password")
            return redirect("login")
        else:
            login(request, user)
            return redirect("receipes")

    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return redirect("register")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Account created successfully")
        return redirect("login")

    return render(request, 'register.html')


def logout_page(request):
    logout(request)
    return redirect("login")

