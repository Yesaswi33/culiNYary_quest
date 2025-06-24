from django.shortcuts import render,redirect
from django.shortcuts import render
from django.http import JsonResponse
from vege.models import Recepie  # Import the model from veg app
from django.core.paginator import Paginator
import json
import os


# Create your views here.
from django.http import HttpResponse

def home(request):
    return render(request, 'home/homepage.html')

def index(request):
    return render(request, 'home/index.html')

def get_dish_data(request):
    import os, json
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'dishes.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return JsonResponse(data, safe=False)




def menu_card(request):
    dishes = Recepie.objects.all()
    return render(request, 'home/menu_card.html', {'dishes': dishes})
