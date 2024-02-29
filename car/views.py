from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from .models import Post, Comment
from django.contrib.auth.models import User
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView, 
                                  UpdateView, 
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request, 'car/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'car/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 8 # determines how many posts in a page

class UserPostListView(ListView):
    model = Post
    template_name = 'car/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(owner = user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['car_name', 'brand', 'content', 'car_image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'car/add_comment.html'
    fields = ['body']
    ordering = ['-date_posted']

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'car/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_pk'] = self.object.post.pk
        return context
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['car_name', 'brand', 'content', 'car_image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self): # only the user who create the post can update the post  -- UserPassesTestMixin
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # after deleting it will redirect to home page

    def test_func(self): # only the user who create the post can delete the post  -- UserPassesTestMixin
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False

def about(request):
    return render(request, 'car/about.html', {'title':'about'})

def post_like(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id = pk)
        if post.likes.filter(id = request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return redirect(reverse('post-detail', kwargs={'pk': pk})) 
        # after liking, it will redirect to the same page where the user liked the post

    else:
        messages.success(request, ("You must be logged in to like!"))
        return redirect('login')    