from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("model",views.cam,name="cam"),
    path("open_cam",views.open_cam,name="open_cam")
]