from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import NewUserForm, CommentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from blog.models import Post


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.shortcuts import render, get_object_or_404

# Create your views here.
class BlogListView(ListView):
    model = Post
    template_name = 'home.html'



class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['title', 'author', 'body']

class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']

class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = NewUserForm()
    return render(request, 'register.html', {'form': form})




def post_detail(request, pk):
	template_name = 'post_detail.html'
	post = get_object_or_404(Post, pk = pk)
	comments = post.comments.filter(active=True)
	new_comment = None
	# Comment posted
	if request.method == 'POST':
	    comment_form = CommentForm(data=request.POST)
	    if comment_form.is_valid():
		
	        # Create Comment object but don't save to database yet
	        new_comment = comment_form.save(commit=False)
	        # Assign the current post to the comment
	        new_comment.post = post
	        # Save the comment to the database
	        new_comment.save()
	else:
	    comment_form = CommentForm()

	return render(request, template_name, {'post': post,
	                                       'comments': comments,
	                                       'new_comment': new_comment,
	                                       'comment_form': comment_form})