from django.test import TestCase, Client
import json

class StringAnalyzerTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_string(self):
        response = self.client.post('/strings', data=json.dumps({'value': 'level'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_strings(self):
        self.client.post('/strings', data=json.dumps({'value': 'test'}), content_type='application/json')
        response = self.client.get('/strings')
        self.assertEqual(response.status_code, 200)
