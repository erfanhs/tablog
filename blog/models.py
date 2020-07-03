from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	followers = models.IntegerField(default=0)
	following = models.IntegerField(default=0)

	def __str__(self):
		return self.user.username

class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	subject = models.CharField(max_length=50)
	content = models.TextField()
	image = models.ImageField()
	created_at = models.DateTimeField(default=timezone.now)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)

	def __str__(self):
		return '{} - {}'.format(self.author.username, self.subject)

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		self.post.likes += 1
		self.post.save()
		super(Like, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.post.likes -= 1
		self.post.save()
		super(Like, self).delete(*args, **kwargs)

	def __str__(self):
		return '{} - {}'.format(self.user.username, self.post.subject)

class Following(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

	def save(self, *args, **kwargs):
		self.user.profile.followers += 1
		self.follower.profile.following += 1
		self.user.profile.save()
		self.follower.profile.save()
		super(Following, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.user.profile.followers -= 1
		self.follower.profile.following -= 1
		self.user.profile.save()
		self.follower.profile.save()
		super(Following, self).delete(*args, **kwargs)

	def __str__(self):
		return '{} - {}'.format(self.user.username, self.follower.username)