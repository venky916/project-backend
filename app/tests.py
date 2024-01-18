from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import App


class RegisterTestCase(APITestCase):
    
    def test_register(self):
        # Test RegisterView
        register_url = reverse('register')  # Update with your register URL
        register_data = {'username': 'newuser','email':"newuser@gmail.com", 'password': 'newpassword'}
        response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "User Registered successsfully")
        
        
class LoginTestCase(APITestCase):
    
    def setUp(self):
        self.client.post(
            reverse('register'),
            {'username': 'newuser1','password': 'newpassword'}
        )
        
    def test_login(self):
        login_url = reverse('knox_login')  # Update with your login URL
        login_data = {'username': 'newuser1', 'email':"newuser@gmail.com",'password': 'newpassword'}
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
class AppAdminTestView(APITestCase):
    
    def setUp(self):
            self.url = reverse("app-list")
            self.authenticate()
            
    def authenticate(self):
        self.client.post(
            reverse('register'),
            {'username': 'newuser','email':"newuser@gmail.com","is_admin":True, 'password': 'newpassword'}
        )

        response = self.client.post(
            reverse('knox_login'),
             {'username': 'newuser', 'password': 'newpassword'},
        )
        # Extract the token from the response
        token_key = response.data['token']

        # Set the token in the client's credentials for future requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_key}')

    def test_AppPost(self):    
        # Create a sample App instance
        app_data = {'app_name': 'Test App', 'points': 10, 'image': None}  # Update with your app data
        response = self.client.post(self.url, app_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Retrieve the created App
        app_id = response.data['id']
        app = App.objects.get(id=app_id)

        # Check if the App instance was created correctly
        self.assertEqual(app.app_name, 'Test App')
        self.assertEqual(app.points, 10)
        # Add more assertions based on your model and serializer
        
    def test_AppGet(self): 
        response=self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_AppGetUnauthenticated(self):
        self.client.force_authenticate(user=None)
        response=self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


class AppNonAdminTestView(APITestCase):
    
    def setUp(self):
            self.url = reverse("app-list")
            self.authenticate()
            
    def authenticate(self):
        self.client.post(
            reverse('register'),
            {'username': 'newuser','email':"newuser@gmail.com",'password': 'newpassword'}
        )

        response = self.client.post(
            reverse('knox_login'),
             {'username': 'newuser', 'password': 'newpassword'},
        )
        # Extract the token from the response
        token_key = response.data['token']

        # Set the token in the client's credentials for future requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token_key}')

    def test_AppPost(self):    
        # Create a sample App instance
        app_data = {'app_name': 'Test App', 'points': 10, 'image': None}  # Update with your app data
        response = self.client.post(self.url, app_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_AppGet(self): 
        response=self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_AppGetUnauthenticated(self):
        self.client.force_authenticate(user=None)
        response=self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)