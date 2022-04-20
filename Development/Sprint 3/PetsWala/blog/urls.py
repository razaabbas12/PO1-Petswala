from django.urls import path
from . import views
from .views import AddCommentView, BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView
urlpatterns = [
    path('', views.home, name='index'),
    path('blog', BlogPostListView.as_view(), name='blog-home'),
    # path('add_product/', views.add_product.as_view(), name='add_product'),
    path('add_new_post/', BlogPostCreateView.as_view(), name='post-create'),
    path('blog/post/<int:pk>/', BlogPostDetailView.as_view(), name='post-detail'),
    path('blog/post/<int:pk>/update/', BlogPostUpdateView.as_view(), name='post-update'),
    path('blog/post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact_us, name='blog-contact-us'),
    path('blog/post/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('blog/search_posts/', views.search_posts, name='search-posts'),
    
]
