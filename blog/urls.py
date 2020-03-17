from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # calls the post_list view when there is no optional parameter
    path('', views.post_list, name='post_list'),
   
    #path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
     # calls the post_list view but when there is an optional param
    # slug: is a slug path converter that converts string to lowecase letters or nums with strings and underscores
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
]