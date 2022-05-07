__author__ = "Tyler Pearson <tdpearson>"
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from rest_framework import status
import time
from api.views import APIRoot, UserProfile
from rest_framework.test import APIClient

class CCAPITest(APITestCase):
    def setUp(self):
        
        self.user = User.objects.create_superuser(
            username='testuser',
        )

        self.user_not_super = User.objects.create_user(
            username='testuser_not_super',
        )
         
        self.apiroot_view = APIRoot.as_view()
        self.userprofile_view = UserProfile.as_view()
        
        self.factory = APIRequestFactory()
    
    def test_api_root(self):
        api_sections = {
            'Queue': {
                'Tasks': 'http://testserver/api/queue/',
                'Tasks History': 'http://testserver/api/queue/usertasks/'
            },
            'Catalog': {
                'Data Source': 'http://testserver/api/catalog/data/'
            },
            'Data Store': {
                'Mongo': 'http://testserver/api/data_store/data/'
            },
            'User Profile': {
                'User': 'http://testserver/api/user/'
            }
        }

        request = self.factory.get('/')
        force_authenticate(request, user=self.user)
        response = self.apiroot_view(request)
        # Confirm the response matches the above api_sections
        self.assertEqual(response.data, api_sections)

    def test_user_profile_logged_in(self):
        request = self.factory.get('/user')
        force_authenticate(request, user=self.user)
        response = self.userprofile_view(request)
        # Confirm the username exists and matches our test user
        self.assertEqual(response.data.get('username'), self.user.username)
        # Confirm that the test user has an auth-token
        self.assertTrue(response.data.get('authentication', {}).get('auth-token'))

    def test_user_profile_not_logged_in(self):
        request = self.factory.get('/user')
        response = self.userprofile_view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    '''
    def test_add_dspace(self):
        args = [2, 3]
        result = 5
        #test_task(self, task, args, result)
        self.client.force_authenticate( user=self.user)
        request = self.client.post( '/queue/run/cybercomq.tasks.tasks.add/', 
            {'queue': 'celery', 'args': [2,3], 'kwargs': {}, 'tags': []}, format = "json")
        url = str(request.data.get('result_url')[21:])
        response = self.client.get(url)
        time.sleep(60)
        self.assertEqual(response.data['result']['status'], 'SUCCESS')
        self.assertEqual(response.data['result']['result'], result)'''

    def test_dspace_add(self):
        task = '/queue/run/dspaceq.tasks.tasks.add/'
        queue = 'dev_dspace'
        args = [2, 3]
        result = 5
        #test_task(self, task, args, result)
        self.client.force_authenticate( user=self.user)
        request = self.client.post(task, 
            {'queue': queue, 'args': args}, format = "json")
        url = str(request.data.get('result_url')[21:])
        response = self.client.get(url)
        self.assertEqual(response.data['result']['result'], result)
'''
#Generic testing functions
def test_reachable_page(self, page):
    request = self.client.get(page)
    self.assertEqual(request.status_code, 401)

def test_task(self, task, args, result):
    self.client.force_authenticate( user=self.user)
    request = self.client.post( task, 
            {'args': args}, format = "json")
    url = str(request.data.get('result_url')[21:])
    response = self.client.get(url)
    print("Result is ", response.data['result']['result'])
    self.assertEqual(response.data['result']['result'], result)'''