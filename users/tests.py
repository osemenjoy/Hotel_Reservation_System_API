from rest_framework.test import APIClient, APITestCase
from .models import User
from django.urls import reverse

class RegisterUserTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("register")

    def test_created_user_successfully(self):
        data = {
            "username" :"test", 
            "password": "testpass", 
            "phone_number":"12345678901", 
            "email":"test@gmail.com"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data["data"]["username"], "test")
        print("User created test succesful 😀")


    def test_user_not_created_successfully(self):
        data = {}
        response = self.client.post(self.url, data, format="json")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(User.objects.count(), 0)
        print("User not created test successful 😆")