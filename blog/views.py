from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserCreateForm, PostCreateForm
from .email import sendConfirmationEmail
from .models import Post, Like, Following


User = get_user_model()


######################
##### USER VIEWS #####
######################


@login_required
def index(request):
	posts = Post.objects.filter(author=request.user)
	return render(request, 'index.html', {'user': request.user, 'posts': posts})


def login(request):
	if request.method == 'POST':
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			auth_login(request, form.user_cache)
			next = request.GET.get('next')
			if not next: next = 'index'
			return redirect(next)
		else:
			return render(request, 'login.html', {'form': form})
	else:
		form = AuthenticationForm()
		return render(request, 'login.html', {'form': form})


def signup(request):
	if request.method == 'POST':
		form = UserCreateForm(request.POST)
		if form.is_valid():
			user = form.save() # create a inactive user
			sendConfirmationEmail(request, user)
			return HttpResponse('<center>We have sent you an email, please confirm your email address to complete registration</center>')
		else:
			return render(request, 'signup.html', {'form': form})
	else:
		form = UserCreateForm()
		return render(request, 'signup.html', {'form': form})


@login_required
def logout(request):
	auth_logout(request)
	return redirect('login')



def profile(request, username):
	if request.user.username == username:
		return redirect('index')
	user = get_object_or_404(User, username=username)
	posts = Post.objects.filter(author=user)
	try:
		Following.objects.get(follower=request.user, user=user)
		follow = True
	except Following.DoesNotExist:
		follow = False
	return render(request, 'profile.html', {'posts': posts, 'user': user, 'follow': follow})




######################
##### POST VIEWS #####
######################



@login_required
def NewPost(request):
	if request.method == 'POST':
		post = Post(author=request.user)
		form = PostCreateForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			form.save()
			return redirect('index')
		else:
			return render(request, 'new_post.html', {'form': form})
	else:
		form = PostCreateForm()
		return render(request, 'new_post.html', {'form': form})


@login_required
def DelPost(request, postid):
	get_object_or_404(Post, id=postid, author=request.user).delete()
	return redirect('index')


def ShowPost(request, postid):
	post = get_object_or_404(Post, id=postid)
	delete = False
	if request.user == post.author:
		delete = True
	try:
		Like.objects.get(user=request.user, post=post)
		like = True
	except Like.DoesNotExist:
		like = False
	post.views += 1
	post.save()
	return render(request, 'post.html', {'post': post, 'like': like, 'delete': delete})



######################
##### LIKE VIEWS #####
######################


@login_required
def SwitchLike(request, postid):
	post = get_object_or_404(Post, id=postid)
	try:
		Like.objects.get(user=request.user, post=post).delete()
	except Like.DoesNotExist:
		Like.objects.create(user=request.user, post=post)
	return redirect(request.META.get('HTTP_REFERER'))


@login_required
def likes(request, postid):
	likes = Like.objects.filter(post__id=postid)
	return render(request, 'likes.html', {'likes': likes})



###########################
##### FOLLOWING VIEWS #####
###########################


@login_required
def followers(request, username):
	user = get_object_or_404(User, username=username)
	followers = Following.objects.filter(user=user)
	return render(request, 'followers.html', {'followers': followers})


def following(request, username):
	user = get_object_or_404(User, username=username)
	following = Following.objects.filter(follower=user)
	return render(request, 'following.html', {'following': following})


def SwitchFollow(request, username):
	user = get_object_or_404(User, username=username)
	if request.user == user:
		return redirect('index')
	try:
		Following.objects.get(follower=request.user, user=user).delete()
	except Following.DoesNotExist:
		Following(follower=request.user, user=user).save()
	return redirect(request.META.get('HTTP_REFERER'))