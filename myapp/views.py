from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import SignUpForm

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,  urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

# Create your views here.
class PostListView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'post/list.html'
	paginate_by = 7

class PostDetailView(DetailView):
	model = Post
	template_name = 'post/detail.html'
	context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = 'post/create.html'
	success_url = reverse_lazy('post-list')
	fields = ('title', 'body')

	def form_valid(self, form):
		post = form.save(commit=False)
		post.author = self.request.user
		post.save()
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
	model = Post
	template_name = 'post/update.html'
	fields = ('title', 'body')

	def get_success_url(self):
		return reverse_lazy('post-detail', kwargs={'pk':self.object.id})

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(author=self.request.user)

class PostDeleteView(LoginRequiredMixin, DeleteView):
	model = Post
	template_name = 'post/delete.html'
	success_url = reverse_lazy('post-list')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(author=self.request.user)

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()

			current_site = get_current_site(request)
			subject = 'Activate your JustPostIt Account '
			message = render_to_string('registration/account_activation_email.html', {
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': account_activation_token.make_token(user),
				})
			user.email_user(subject, message)
			return redirect('account_activation_sent')
	else:
		form = SignUpForm()
	return render(request, 'registration/signup.html',{'form':form})


def account_activation_sent(request):
	return render(request, 'registration/account_activation_sent.html')

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)

	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return redirect('post-list')

	else:
		return render(request, 'registration/account_activation_invalid.html')