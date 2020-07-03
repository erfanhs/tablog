from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import login as auth_login
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .models import Profile
import six


User = get_user_model()


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()


def sendConfirmationEmail(request, user):
	current_site = get_current_site(request)
	email_subject = 'erlog | Activate Your Account'
	message = render_to_string('acc_active_email.html', {
		'user': user,
		'domain': current_site.domain,
		'uid': urlsafe_base64_encode(force_bytes(user.id)),
		'token': account_activation_token.make_token(user)
	})
	to_email = user.email
	email = EmailMessage(email_subject, message, to=[to_email])
	email.send()


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(id=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		Profile.objects.create(user=user)
		auth_login(request, user)
		return HttpResponse('<center>Your account has been activate successfully</center>')
	else:
		return HttpResponse('<center>Activation link is invalid!</center>')