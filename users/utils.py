import six
import threading
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


#TODO: Store token in the db for 15 minutes. If token exists use it. If 15 minutes are up regenerate a new token.
class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_verified))
    

generate_token = EmailVerificationTokenGenerator()

class SendEmail:
    def create_email():
        pass

    @staticmethod
    def send_activation_email(request, user):
        current_site = get_current_site(request)
        email_subject = 'Activate your account'
        email_body = render_to_string('users/email_verification_template.html', {
            'user':user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
            })

        thread = threading.Thread(target=send_mail, kwargs={'subject':email_subject, 'message':email_body, 'from_email':settings.EMAIL_FROM_USER, 'recipient_list':[user.email], 'html_message':email_body})
        thread.start()