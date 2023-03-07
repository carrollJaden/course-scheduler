from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.contrib import auth
import requests

#setup test cases
class setUpTestCase(TestCase):
    def test_user_not_logged_in(self):
        response = self.client.get('/about', follow=True)
        self.assertEqual(response.redirect_chain[0][0], "/about/")
    
    def unauth_user_logged_in(self):
        c = Client()
        User.objects.create_user(username='stream', password='lg')
        c.login(username='stream', password='lg')
        response = self.client.get('/about', follow=True)
        self.assertTrue(response.redirect_chain[0][0], "/about/")

    def test_drop_down_course_selection(self):
        c = Client()
        User.objects.create_user(username='admin', password='admin')
        c.login(username='admin', password='admin')
        response = self.client.get('/about', follow=True)
        self.assertTrue(response.redirect_chain[0][0], "/about/")
        
#Google login test
class googleLoginTestCase(TestCase):
    def test_user_not_logged_in(self):
        response = self.client.get('/about', follow=True)
        self.assertEqual(response.redirect_chain[0][0], "/about/")
        
#Unauthorized login
class unauthLoginTestCase(TestCase):
    def unauth_user_logged_in(self):
        c = Client()
        User.objects.create_user(username='stream', password='lg')
        c.login(username='stream', password='lg')
        response = self.client.get('/profiles', follow=True)
        self.assertTrue(response.redirect_chain[0][0], "/about/")

#Unauthorized login 2
class unauthLoginTestCaseTwo(TestCase):
    def unauth_user_logged_in(self):
        c = Client()
        User.objects.create_user(username='stream', password='lg')
        c.login(username='stream', password='lg')
        response = self.client.get('/profiles', follow=True)
        self.assertFalse(response.redirect_chain[0][0], "/services/")

#dropdown menu
class dropdownMenuTestCase(TestCase):
    def unauth_user_logged_in(self):
        c = Client()
        User.objects.create_user(username='admin', password='admin')
        c.login(username='admin', password='admin')
        response = self.client.get('/about', follow=True)
        self.assertFalse(response.redirect_chain[0][0], "/services/")

#classesByDept
class classesByDeptTestCase(TestCase):
    def listed_classes(self):
        c = Client()
        User.objects.create_user(username='admin', password='admin')
        c.login(username='admin', password='admin')
        subjectData = requests.get('http://luthers-list.herokuapp.com/api/deptlist?format=json').json()
        for subject in subjectData:
            response = requests.get('http://luthers-list.herokuapp.com/api/dept/' + subject['subject'] + '/?format=json').json()
            self.assertFalse(len(response) == 0)
