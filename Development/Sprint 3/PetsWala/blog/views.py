from audioop import reverse
from django import urls
from django.forms import SlugField
from django.shortcuts import render, redirect, get_object_or_404

from blog.forms import CommentForm
from .models import Post, Comment
from accounts.form import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
# from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse



def home(request):
    return render(request, 'blog/index.html')

def blog(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Home',
        }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html')

def contact_us(request):
    return render(request, 'blog/contact.html')

# def detail(request, slug):
#     post = Post.objects.get(slug=slug)

#     if request.method == 'POST':
#         form = CommentForm(request.POST)

#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.post = post
#             obj.save()

#             return redirect('post-detail', slug=post.slug)
#     else:
#         form = CommentForm()


#     context = {
#         'post':post,
#         'form':form
#     }

#     return render(request, 'blog/post_detail.html', context)



class BlogPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class BlogPostDetailView(DetailView):
    model = Post
    



class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # form_class = AddNewPost

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    # form_class = AddNewPost

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class AddCommentView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    model = Comment
    fields = ['body']
    success_url = urls.reverse_lazy('blog-home')
    success_message = 'New Comment Added'
    
    def form_valid(self, form):
        form.instance.name = self.request.user
        post = Post.objects.get(id=self.kwargs.get('pk'))
        form.instance.post = post
        #blog_comment.post_id = self.pk_url_kwarg
        #post = Post.objects.get(pk=self.request.POST.get('pk'))
        
        return super().form_valid(form)
    
    

    