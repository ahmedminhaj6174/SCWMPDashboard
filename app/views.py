from django.shortcuts import render

# Create your views here.

# creating an index function

def index(request):
    return render(request, "index.html")

def datatables(request):
    return render(request, "datatables.html")
