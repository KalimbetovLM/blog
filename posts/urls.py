from django.urls import path
from posts.views import PostView,PostDetail,CreatePostView,WeeklyPopularPosts,MonthlyPopularPosts, \
RecommendedPostsView,PopularPostsView

app_name='posts'
urlpatterns = [
    path('list/',PostView.as_view(),name='post_list'),
    path('<int:pk>/',PostDetail.as_view(),name='post_detail'),
    path('create/',CreatePostView.as_view(),name='post_create'),
    path('weekend/',WeeklyPopularPosts.as_view(),name='weekend'),
    path('month/',MonthlyPopularPosts.as_view(),name='month'),
    path('recommended/',RecommendedPostsView.as_view(),name='recommended'),
    path('popular/',PopularPostsView.as_view(),name='popular')
]