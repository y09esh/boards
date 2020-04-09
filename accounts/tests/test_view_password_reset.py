from django.contrib.auth.tokens import default_token_generator as token_gen
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode as urlsafe64en
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse, resolve
from django.test import TestCase

class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)
    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)
    def test_view_function(self):
        view = resolve('/reset/')
        self.assertEquals(view.func.view_class,auth_views.PasswordResetView)
    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')
    def test_contains_form(self):
        form =self.response.context.get('form')
        self.assertIsInstance(form,PasswordResetForm)
    def test_form_inputs(self):
        self.assertContains(self.response,'<input',2)
        self.assertContains(self.response,'type="email"',1)
class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'john@example.com'
        User.objects.create_user(username='john', email=email, password='123abcdef')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))

class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response=self.client.get(url)
    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)
    def test_view_function(self):
        view = resolve('/reset/complete/')
        self.assertEquals(view.func.view_class,auth_views.PasswordResetCompleteView)

class PasswordResetDoneTest(TestCase):
    def setUp(self):
        self.response =self.client.get(reverse('password_reset_done'))
    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)
    def test_view_function(self):
        view = resolve('reset/done/')
        self.assertEquals(view.func.view_class,auth_view.passwordResetDoneView)

class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='example', email = 'non@example.com',PasswordResetCompleteTests='jhgjhyfdhj1324')
        self.uid = urlsafe64en(force_bytes(user.pk)).decode()
        self.token = token_gen.make_token(user)
        url = reverse('password_reset_confirm', kwargs={'uid64':self.uid,'token':self.token})
        self.response = self.client.get(url,follow=True)
    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)
    def test_view_function(self):
        view = resolve('/reset/{uidb64}/{token}/'.format(uidb64=self.uid,token=self.token))
        self.assertEquals(view.func.view_class,auth_views.PasswordResetConfirmView)
    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')
    def test_contains_for(self):
        form = self.response.context.get('form')
        self.assertInInstance(form,SetPasswordForm)
    def test_form_inputs(self):
        self.assertContains(self.response,'<input',3)
        self.assertContains(self.response,'type="password"',2)

class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='example', email = 'non@example.com',PasswordResetCompleteTests='jhgjhyfdhj1324')
        uid = urlsafe64en(force_bytes(user.pk)).decode()
        token = token_gen.make_token(user)
        user.set_password('ashgdagsagl242342')
        url = reverse('password_reset_confirm', kwargs={'uid64':self.uid,'token':self.token})
        self.response = self.client.get(url,follow=True)
    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)
    def test_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response,'invalid password reset link')
        self.assertContains(self.response,'href="{0}"'.format(password_reset_url))