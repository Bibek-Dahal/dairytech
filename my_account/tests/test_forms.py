from django.test import TestCase,RequestFactory
from my_account.models import User
from my_account.forms import *
from django.http import HttpRequest
class TestMyUserCreationForm(TestCase):
    def setUp(self):
        
        self.data = {
            'email':'johndoe@gmail.com',
            'phone_number':'9864554432',
            'first_name':'john',
            'middle_name':'prasad',
            'last_name':'doe',
            'password1':'Admin@123',
            'password2':'Admin@123'
        }

        
        self.user = User.objects.create_user(
            email='johndoe1@gmail.com',
            phone_number='9864554422',
            first_name='john',
            middle_name='prasad',
            last_name='doe',
            password='Admin@123'
        )
        
    def test_valid_user_data(self):
        form = MyUserCreationForm(data=self.data)
        self.assertTrue(form.is_valid())
        
        
    
    def test_password_less_than_eight_char_and_too_common(self):
        self.data['password1']='Admin'
        form = MyUserCreationForm(data=self.data)
        self.assertFalse(form.is_valid())
        
        self.assertEqual(form.errors['password1'],[
            'This password is too short. It must contain at least 8 characters.',
            "This password is too common."
        ])
    
    def test_password_mismatch(self):
        self.data['password1'] = 'Admin@123'
        self.data['password2'] = 'Admin@1234'
        form = MyUserCreationForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertListEqual(form.errors['password2'],['You must type the same password each time.'])

    def test_password_doesnot_contain_special_chars_and_numbers(self):
        self.data['password1'] = 'AdminAdmin'
        self.data['password2'] = 'AdminAdmin'
        form = MyUserCreationForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertListEqual(form.errors['password1'],['Password must contain at least one digit, special characrers and uppercase letter'])

    def test_required_field_not_providing_error(self):
        data = {
            
        }
        form = MyUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

        self.assertListEqual(form.errors['email'],['This field is required.'])
        self.assertListEqual(form.errors['first_name'],['This field is required.'])
        self.assertListEqual(form.errors['last_name'],['This field is required.'])
        self.assertListEqual(form.errors['phone_number'],['This field is required.'])
        self.assertListEqual(form.errors['password1'],['This field is required.'])
        self.assertListEqual(form.errors['password2'],['This field is required.'])

    def test_user_with_email_already_exists(self):
        data = {
            'email':'johndoe1@gmail.com',
            'first_name':'john',
            'middle_name':'prasad',
            'last_name':'doe',
            'phone_number':'9864554422',
            'password1':'Admin@123',
            'password2':'Admin@123'
        }
        form = MyUserCreationForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertListEqual(form.errors['email'],['User with email address already exists.'])
        
    def test_user_with_phone_number_already_exists(self):
        data = {
            'email':'johndoe223@gmail.com',
            'first_name':'john',
            'middle_name':'prasad',
            'last_name':'doe',
            'phone_number':'9864554422',
            'password1':'Admin@123',
            'password2':'Admin@123'
        }
        form = MyUserCreationForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertListEqual(form.errors['phone_number'],['User with phone numbre already exists'])

class TestMyLoginForm(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='johndoe1@gmail.com',
            phone_number='9864554422',
            first_name='john',
            middle_name='prasad',
            last_name='doe',
            password='Admin@123'
        )
        

    def test_login_credintal(self):
        request = self.factory.get("/en/accounts/login")
        data = {
            'login':'johndoe1@gmail.com',
            'password':'Admin@123',
            'remember':True
        }
        form = MyLoginForm(data=data,request=request)
        self.assertTrue(form.is_valid())

class TestMyPasswordChangeForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='johndoe1@gmail.com',
            phone_number='9864554422',
            first_name='john',
            middle_name='prasad',
            last_name='doe',
            password='Admin@123'
        )



    def test_valid_login_form(self):
       
        data = {
            'oldpassword':'Admin@123',
            'password1':'Admin@1234',
            'password2':'Admin@1234'
        }
        form = MyPasswordChangeForm(user=self.user,data=data)
        print("form errors===",form.errors)
        self.assertTrue(form.is_valid())

    