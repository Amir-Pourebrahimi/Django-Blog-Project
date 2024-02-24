from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic

from .forms import PostForm
from .models import Post


class PostListView(generic.ListView):
    # model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('-date_modified')


# def post_list_view(request):
#     # post_list = Post.objects.all()
#     post_list = Post.objects.filter(status='pub').order_by('-date_modified')
#     return render(request, 'blog/posts_list.html', {'post_list': post_list})

class PostDetailView(generic.DetailView):
    model = Post  # this model name automatically set context_name : post / ex) Comment : comment
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


# def post_detail_view(request, pk):
#     # post = Post.objects.get(pk=pk)
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})

class PostCreateView(generic.CreateView):
    form_class = PostForm
    template_name = 'blog/create_post.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['author'].queryset = User.objects.filter(id=self.request.user.id)
        return form


# def post_create_view(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             form = PostForm()
#             return redirect('posts_list')
#
#     else:
#         form = PostForm()
#
#     return render(request, 'blog/create_post.html', context={'form': form})

# if request.method == 'POST':
#     title = request.POST.get('title')
#     text = request.POST.get('text')
#
#     user = User.objects.all()[0]
#     Post.objects.create(title=title, text=text, author=user, status='pub')
# else:
#     print('Get Method')
# return render(request, 'blog/create_post.html')

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'


# def post_update_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     form = PostForm(request.POST or None, instance=post)
#     if form.is_valid():
#         form.save()
#         return redirect('posts_list')
#
#     return render(request, 'blog/create_post.html', context={'form': form})
#

class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('posts_list')

    # def get_success_url(self):

# def post_delete_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         post.delete()
#         return redirect('posts_list')
#
#     return render(request, 'blog/delete_post.html', context={'post': post})
