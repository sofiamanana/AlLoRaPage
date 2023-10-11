from django.urls import path

from . import views

urlpatterns = [
    path("getNodos/", views.getNodos, name="getNodos"),
    path("", views.getGateway, name="getGateway"),
    path("addNode/", views.addNode, name="addNode"),
    path("index/", views.index, name="index")


]