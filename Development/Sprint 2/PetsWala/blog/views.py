from django.shortcuts import render
from .models import Post
from accounts.form import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
# from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from django.http import HttpResponse



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
