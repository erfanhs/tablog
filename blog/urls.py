from django.urls import path

from .views import *
from .email import activate

urlpatterns = [
	path('', index, name='index'),
	path('login/', login, name='login'),
	path('signup/', signup, name='signup'),
	path('logout/', logout, name="logout"),
	path('activate/<uidb64>/<token>/', activate, name='activate'),

	path('new-post/', NewPost, name='NewPost'),
	path('delete-post/<int:postid>/', DelPost, name='DelPost'),

	path('post/<int:postid>/', ShowPost, name='ShowPost'),

	path('switch-like/<int:postid>/', SwitchLike, name='SwitchLike'),
	path('likes/<int:postid>/', likes, name="likes"),

	path('<str:username>/', profile, name='profile'),

	path('followers/<str:username>/', followers, name='followers'),
	path('following/<str:username>/', following, name='following'),
	path('switch-follow/<str:username>/', SwitchFollow, name='SwitchFollow')
]