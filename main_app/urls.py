from django.urls import path
# additional imports # additional imports
from .views import Home, CatList, CatDetail, FeedingListCreate, FeedingDetail, ToyList, ToyDetail

urlpatterns = [
    # home route lives here
    path('', Home.as_view(), name='home'),
    # new routes below 
    path('cats/', CatList.as_view(), name='cat-list'),
    path('cats/<int:id>/', CatDetail.as_view(), name='cat-detail'),
    path('cats/<int:cat_id>/feedings/', FeedingListCreate.as_view(), name='feeding-list-create'),
	path('cats/<int:cat_id>/feedings/<int:id>/', FeedingDetail.as_view(), name='feeding-detail'),
    path('toys/', ToyList.as_view(), name='toy-list'),
    path('toys/<int:id>/', ToyDetail.as_view(), name='toy-detail'),
]