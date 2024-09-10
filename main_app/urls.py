from django.urls import path
from .views import Home, CatList, CatDetail # additional imports

urlpatterns = [
    path('', Home.as_view(), name='home'),
    # new routes below 
    path('cats/', CatList.as_view(), name='cat-list'),
    path('cats/<int:id>/', CatDetail.as_view(), name='cat-detail'),
]