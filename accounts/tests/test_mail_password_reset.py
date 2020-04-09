from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

class PasswordresetMailTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='example_',email='non@exaple.com',password='kuchbhi123')
        self.response=self.client.post(reverse('password_reset'),{'email':'non@example.com'})
        self.email=mail.outbox[0]
    def test_email_subject(self):
        self.assertEquals('[Django Boards] Please reset your password',self.email.subject)
    def test_email_body(self):
        context=self.response.context
        token=context.get('token')
        uid=context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm',kwargs={
            'uidb64':uid,
            'token':tiken
            })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('example',self.eamil.body)
        self.assertIn('non@example.com',self.email.body)
    def test_email_to(self):
        self.assertEqual(['non@example.com',],slef.email.to)