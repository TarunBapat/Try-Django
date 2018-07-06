from django.urls import path,include
from . import views


app_name="posts"
urlpatterns = [
    path('',views.post_home),
    path('create/',views.post_create,name="create"),
    path('list/',views.post_list,name='list'),
    path('<int:id>/',views.post_detail,name="detail"),
    path('<int:id>/edit/',views.post_update),
    path('<int:id>/delete/',views.post_delete,name="delete")
]