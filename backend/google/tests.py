import json
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.conf import settings
from django.test.utils import override_settings

from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from cr_search.models import SavedSearch

@override_settings(ES_INDEX = {'CCDB': 'complaints_test_ccdb','CRDB' : 'complaints_test_crdb'})
class SearchTest(APITestCase):
    fixtures = ['test_users']

    def setUp(self):
        self.client.login(username='john.smith', password='123456')
        self.end_point = '/_search'

    def test_search(self):
        expected_index_name = settings.ES_INDEX['CRDB']
        data = {"query":
                    {"term":
                         {"what_happened": "test"}
                     }
                }
        body = {"search": data, "search_term": "test", "params" : "testParams"}
        response = self.client.post(self.end_point, body, format='json')
        results = json.loads(response.content)
        total = results['hits']['total']
        actual_index_name = results['hits']['hits'][0]['_index']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(total, 0)
        self.assertEqual(expected_index_name, actual_index_name)

    def test_search_routing_with_index_name_param(self):
        expected_index_name = settings.ES_INDEX['CCDB']
        data = {"query":
                    {"term":
                         {"what_happened": "test"}
                     }
                }
        params = {"index_name": expected_index_name}
        body = {"search": data, "search_term": "test", "params" : params}
        response = self.client.post(self.end_point, body, format='json')
        results = json.loads(response.content)
        actual_index_name = results['hits']['hits'][0]['_index']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_index_name, actual_index_name)

    def test_search_routing_with_bad_index_name_param(self):
        self.client.login(username='joe.bob', password='123456')
        expected_index_name = settings.ES_INDEX['CRDB']
        data = {"query":
                    {"term":
                         {"what_happened": "test"}
                     }
                }
        params = {"index_name": expected_index_name}
        body = {"search": data, "search_term": "test", "params" : params}
        response = self.client.post(self.end_point, body, format='json')
        self.assertEqual(response.status_code, 403)

    def test_search_w_bad_body(self):
        data = {"query": {"query": "test"}}
        body = {"search": data, "search_term": "test", "params" : "testParams"}
        response = self.client.post(self.end_point, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Parse Failure [Failed to parse source', response.data['error'])

@override_settings(ES_INDEX = {'CCDB': 'complaints_test_ccdb','CRDB' : 'complaints_test_crdb'})
class ExportTest(TestCase):
    fixtures = ['test_users']

    def setUp(self):
        self.client = Client()
        self.client.login(username='john.smith', password='123456')
        self.end_point = '/_export'

    def test_bad_format(self):
        fmt = "jpg"
        search = {"body":{"query":{"match": {"severity":"good"}},"_source": ["severity","text"]}}
        body = {"format": fmt, "search": search, "search_term": "test", "params" : "testParams"}
        response = self.client.get(self.end_point, body)
        self.assertEqual(response.status_code, 400)
        msg = {"error": "format %s not supported" % fmt}
        self.assertEqual(response.content, json.dumps(msg))

    def test_export_bad_body(self):
        """
        query in the wrong format should fail
        """
        fmt = "csv"
        search = {"querya": {"match": {"severity":"good"}}, "_source": ["severity","text"]}
        body1 = {"format": fmt, "search": json.dumps(search), "search_term": "test", "params" : "testParams"}
        response = self.client.get(self.end_point, body1)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('No parser for element [querya]', response.content)

        body2 = {"format": fmt, "search": "abcd", "search_term": "test", "params" : "testParams"}
        response = self.client.get(self.end_point, body2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('query body not in right format', response.content)

    def test_export_csv(self):
        fmt = "csv"
        search = {"query": {"match": {"what_happened":"bank"}}, "_source": ["severity","text"]}
        body = {"format": fmt, "search": json.dumps(search), "search_term": "test", "params" : "testParams"}
        response = self.client.get(self.end_point, body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.content), 0)

    def test_export_json(self):
        fmt = "csv"
        search = {"query": {"match": {"what_happened":"bank"}}, "_source": ["severity","text"]}
        body = {"format": fmt, "search": json.dumps(search), "search_term": "test", "params" : "testParams"}
        response = self.client.get(self.end_point, body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.content), 0)

    def test_export_csv_no_null_body(self):
        fmt = "csv"
        body = {"format": fmt}

        response = self.client.get(self.end_point, body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        msg = {"error": "you must provide a query body"}
        self.assertEqual(response.content, json.dumps(msg))

    def test_export_bad_index_name_param(self):
        self.client.login(username='joe.bob', password='123456')
        expected_index_name = settings.ES_INDEX['CRDB']
        params = json.dumps({"index_name": expected_index_name})
        fmt = "csv"
        search = {"query": {"match": {"what_happened":"bank"}}, "_source": ["severity","text"]}
        body = {"format": fmt, "search": json.dumps(search), "search_term": "test", "params" : params}
        response = self.client.get(self.end_point, body, format='json')
        self.assertEqual(response.status_code, 403)

@override_settings(ES_INDEX = {'CCDB': 'complaints_test_ccdb','CRDB' : 'complaints_test_crdb'})
class SuggestTest(APITestCase):
    fixtures = ['test_users']

    def setUp(self):
        self.client.login(username='john.smith', password='123456')
        self.end_point = '/_suggest'

    def test_must_have_text(self):
        response = self.client.post(self.end_point)
        msg = {"error":"text key is missing"}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), msg)

    def test_suggest(self):
        body = {"text": "b", "size": 3}
        response = self.client.post(self.end_point, body)
        results = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 3)

@override_settings(ES_INDEX = {'CCDB': 'complaints_test_ccdb','CRDB' : 'complaints_test_crdb'})
class SaveTest(APITestCase):
    fixtures = ['test_users']

    def setUp(self):
        self.client.login(username='john.smith', password='123456')
        self.test_user = User.objects.get(username='john.smith')
        self.test_search = SavedSearch.objects.create(user=self.test_user, name='testSave',
            time=datetime.now(), data="testData", search_term="testSearch",
            params="params")

    def test_save_search(self):
        self.end_point = '/_search/save'
        data = {"query":
            {"term":
                 {"what_happened": "test"}
             }
        }
        body = {"name":"testSave", "search": data,
        "search_term": "test", "params" : "testParams"}
        response = self.client.post(self.end_point, body, format='json')
        msg = "Saved Successfully"
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, msg)
        self.assertEqual(SavedSearch.objects.all().count(), 2)

    def test_save_fails_get_request(self):
        self.end_point = '/_search/save'
        data = {"query":
            {"term":
                 {"what_happened": "test"}
             }
        }
        body = {"name":"testSave", "search": json.dumps(data),
        "search_term": "test", "params" : "testParams"}
        response = self.client.get(self.end_point, body, format='json')
        msg = "This endpoint only accepts POST request"
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, msg)

    def test_save_fails_missing_params(self):
        self.end_point = '/_search/save'
        body = {}
        response = self.client.post(self.end_point, body, format='json')
        msg = "Error while saving! Invalid request body."
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, msg)

    def test_get_saved_search(self):
        self.end_point = '/_search/get'
        body = {"limit" : "2"}
        response = self.client.get(self.end_point, body)
        self.assertEqual(response.status_code, 200)

    def test_get_saved_search_post_error(self):
        self.end_point = '/_search/get'
        body = {"limit" : "2"}
        response = self.client.post(self.end_point, body)
        msg = "This endpoint only accepts GET request"
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, msg)
