import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Server.server import app

class Test(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SERVER_NAME'] = 'localhost:8082'
        self.app = app.test_client()
    
    def test_InvalidUser1(self):
        response = self.app.get('/recommend/-1')
        print(response.request.url)
        self.assertEqual(response.status_code, 200)
        result = response.data.decode('utf-8')
        print(result)
        self.assertEqual(result, "Invalid user")

    def test_InvalidUser2(self):
        response = self.app.get('/recommend/0')
        print(response.request.url)
        self.assertEqual(response.status_code, 200)
        result = response.data.decode('utf-8')
        print(result)
        self.assertEqual(result, "Invalid user")

    def test_InvalidUser3(self):
        response = self.app.get('/recommend/weirdstring')
        print(response.request.url)
        self.assertEqual(response.status_code, 200)
        result = response.data.decode('utf-8')
        print(result)
        self.assertEqual(result, "Invalid user")

    def test_ValidUser4070(self):
        response = self.app.get('/recommend/4070')
        print(response.request.url)
        self.assertEqual(response.status_code, 200)
        result = response.data.decode('utf-8')
        print("Returned Movies for user : 4070")
        print(result)

        # if response.status_code == 200:
        #     result = response.data.decode('utf-8')
        #     expectlength = result.split(',')
        #     self.assertEqual(expectlength, 20)

    def test_ValidUser4069(self):
        response = self.app.get('/recommend/4069')
        print(response.request.url)
        self.assertEqual(response.status_code, 200)
        result = response.data.decode('utf-8')
        print("Returned Movies for user : 4069")
        print(result)
    

if __name__ == '__main__':
    unittest.main()