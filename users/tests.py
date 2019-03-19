from django.test import TestCase
from django.contrib.auth.forms import User
from .forms import *


class UserRegisterFormTest(TestCase):
    def test_register_form_valid(self):
        register_data = {
            'username': 'testingform',
            'email': 'test@test.com',
            'password1': 'testing321',
            'password2': 'testing321',
        }
        form = UserRegisterForm(data=register_data)
        self.assertTrue(form.is_valid())

    def test_register_form_different_passwords(self):
        register_data = {
            'username': 'testingform',
            'email': 'test@test.com',
            'password1': 'testing123',
            'password2': 'testing321',
        }
        form = UserRegisterForm(data=register_data)
        self.assertFalse(form.is_valid())

    def test_register_form_weak_password(self):
        register_data = {
            'username': 'testingform',
            'email': 'test@test.com',
            'password1': 'xyz',
            'password2': 'xyz',
        }
        form = UserRegisterForm(data=register_data)
        self.assertFalse(form.is_valid())

    def test_register_form_user_already_exists(self):
        user = User.objects.create_user(username='testingform')
        register_data = {
            'username': 'testingform',
            'email': 'test@test.com',
            'password1': 'testing123',
            'password2': 'testing321',
        }
        form = UserRegisterForm(data=register_data)
        self.assertFalse(form.is_valid())
