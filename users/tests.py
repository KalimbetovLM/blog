from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user
from django.contrib.auth.models import User

# Create your tests here.

class UsersTestCase(TestCase):

    def test_user_registered(self):

        self.client.post(
            reverse('users:register'),
            data={
                "username":"User",
                "first_name":"Userbek",
                "last_name":'Userbekov',
                "email":"user@gmail.com",
                "password":"password12345"
            }
        )
        user = User.objects.get(username="User")
        users_count = User.objects.count()
        
        self.assertEqual(users_count,1)
        self.assertEqual(user.username,"User")
        self.assertEqual(user.first_name,"Userbek")
        self.assertEqual(user.last_name,"Userbekov")
        self.assertEqual(user.email,"user@gmail.com")
        self.assertNotEqual(user.password,"password12345")
        self.assertTrue(user.check_password("password12345"))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                "first_name":"Userbek",
                "last_name":"Userov",
                "email":"user@gmail.com",                
            }
        )
        form = response.context['form']
        user_count = User.objects.count()

        self.assertEqual(user_count,0)
        self.assertFormError(form,'username','This field is required.')
        self.assertFormError(form,"password","This field is required.")

    

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                "username":"User",
                "first_name":"Userbek",
                "last_name":"Userov",
                "email":"invalid_email",
                "password":"password12345"                
            }
        )
        user_count = User.objects.count()
        form = response.context['form']

        self.assertEqual(user_count,0)
        self.assertFormError(form,'email','Enter a valid email address.')

    def test_username_is_unique(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username':'User',
                "first_name":"userbek",
                "last_name":"Userov",
                "email":"user@gmail.com",
                "password":"password12345"
            })
        
        response = self.client.post(
            reverse("users:register"),
            data={
                "username":"User",
                "first_name":"Userjon",
                "last_name":"Userjonov",
                "email":"userjon@gmail.com",
                "password":"password54321"
            }
        )
        users_count = User.objects.count()
        form = response.context['form']

        self.assertEqual(users_count,1)
        self.assertFormError(form,"username","A user with that username already exists.")

class LoginTestCase(TestCase):
    
    def test_user_logged_in(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username":"User",
                "first_name":"Userbek",
                "last_name":"Userov",
                "email":"user@gmail.com",
                "password":"password12345"
            }
        )
        self.client.post(
            reverse("users:login"),
            data={
                "username":"User",
                "password":"password12345"
            }
        )
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_login_with_wrong_credentials(self):
        self.client.post(
            reverse("users:register"),
            data={
                'username':'User',
                'first_name':'Userbek',
                'last_name':'Userov',
                'email':'user@gmail.com',
                'password':'password12345'
            }
        )

        response = self.client.post(
            reverse('users:login'),
            data={
                'username':'User',
                'password':'wrongPassword'
            }
        )
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)
        self.assertContains(response,"Please enter a correct username and password.")
    
    def test_logging_out(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username':'user',
                'password':'passwrod12345'
            }
        )

        self.client.post(
            reverse('users:login'),
            data={
                "usernmae":"user",
                "password":"password12345"
            }
        )
    
        self.client.get(reverse('users:logout'))

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)





