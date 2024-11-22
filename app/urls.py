from django.urls import path
from . import views

urlpatterns = [
    path("datatables", views.datatables, name="app-datatables"),
    path("", views.index, name="app-index")
    
]