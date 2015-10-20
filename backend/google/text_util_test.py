import json
from unittest import TestCase, main
from datetime import datetime
import numpy as np
from elasticsearch import Elasticsearch
from sklearn.datasets import fetch_20newsgroups
from elasticsearch.helpers import bulk, scan
from text_util import text_similarity_scores, text_similarity_score_by_content, text_similarity_score_by_id, text_similarity_score_by_json, index_text

def random_sample_by_pct(a,pct):
    """
    randomly pct(<= 1.0)  sample without replacement from the list a
    """
    n = len(a)
    np.random.seed(4)
    idx = np.random.random(n) < pct 
    return [a[i] for i in range(n) if idx[i]]

class TextDuplicationTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Make a dataset for testing; doc i and doc 100+i are 90% the same
        """
        # make some duplicated documents from sklearn/newsgroup data. 
        categories = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']
        twenty_train = fetch_20newsgroups(subset='train',categories=categories, shuffle=True, random_state=42)
        data_size = 100
        cls._data_size = data_size
        sample_pct = 0.9
        new_data = [' '.join(random_sample_by_pct(data.split(" "), sample_pct)) for data in twenty_train.data[:data_size]]
        data_to_insert = new_data + twenty_train.data[:data_size]

        es = Elasticsearch()
        cls._es = es
        actions = []
        for i,data in enumerate(data_to_insert):
            actions.append({'_id':i, '_source':{'text':data}})
        cls._index_name = "textsimilaritytest"
        cls._doc_type_name = "newsgroup"
        rv = bulk(es,actions,stats_only=True,index=cls._index_name , doc_type=cls._doc_type_name, refresh=True) #default action is 'index'
        assert(rv[1] == 0)  # assert no failure
        rv = es.search(index=cls._index_name, doc_type=cls._doc_type_name, body={"query":{"match_all":{}}},search_type="count")
        assert(rv['hits']['total'] == len(data_to_insert))

    def test_index_text(self):
        """
        test index_text 
        """
        text =  "Quotes are real-time for NASDAQ, NYSE.\n  Yahoo! has not reviewed, and in no way endorses the validity of such data. Yahoo! and ThomsonFN shall not be liable for any actions taken in reliance thereon."
        obj_json = json.dumps({ "id": 3, "title": "IBM: Summary for International Business Machines- Yahoo! Finance", "url": "http://finance.yahoo.com/q?s=IBM", "snippet": "2 days ago ... View the basic IBM stock chart on Yahoo! Finance. Change the date range, chart \ntype and compare International Business Machines against ...", "rank": 2, "text": text, "docType": "", "label": 0, "createdAt": "2015-10-11T21:49:37.797821Z", "search": 1 })
        index_text(index = self._index_name, doc_type="indextest",obj_json=obj_json)
        es = self._es
        rv = es.get(index=self._index_name, doc_type="indextest", id = 3)
        self.assertEqual(rv['_source']['text'], text)
        return 

    def test_similarity_scores(self):
        """
        test text_util.text_similarity_scores() on a synthetic dataset
        """
        #test whether duplications are identified. 
        rv_mat = text_similarity_scores(index = self._index_name, doc_type = self._doc_type_name, mlt_fields=['text'])
        self.assertTrue((np.abs(rv_mat.row-rv_mat.col)== self._data_size).all())
        return 
    
    def test_similarity_score_by_content(self):
        es = self._es
        rv = es.get(index=self._index_name, doc_type=self._doc_type_name, id = 0)
        like_text = rv['_source']['text']
        r_id, _ = text_similarity_score_by_content(index=self._index_name, doc_type=self._doc_type_name, content=like_text, fields=['text'], stop_words=[u"is",u"a"])
        self.assertEqual(r_id, 0)
        return 
    
    def test_similarity_score_by_content_no_match(self):
        es = self._es
        rv = es.get(index=self._index_name, doc_type=self._doc_type_name, id = 0)
        like_text = rv['_source']['text']
        r_id, _ = text_similarity_score_by_content(index=self._index_name, doc_type=self._doc_type_name, content="aaHello aaWorld", fields=['text'], stop_words=[u"is",u"a"])

        self.assertEqual(r_id, -1)
        return 

    def test_similarity_score_by_json(self):
        es = self._es
        rv = es.get(index=self._index_name, doc_type=self._doc_type_name, id = 0)
        obj_json = json.dumps(rv['_source'])
        new_obj_json = text_similarity_score_by_json(index=self._index_name, doc_type=self._doc_type_name, obj_json=obj_json, fields=['text'], stop_words=[u"is",u"a"])
        r_id = json.loads(new_obj_json)["similar_to"]
        self.assertEqual(r_id, 0)
        return 

    def test_similarity_score_by_json_no_match(self):
        es = self._es
        obj_json = json.dumps({'text': "aaaHello aaaWorld"})
        new_obj_json = text_similarity_score_by_json(index=self._index_name, doc_type=self._doc_type_name, obj_json=obj_json, fields=['text'], stop_words=[u"is",u"a"])
        r_id = json.loads(new_obj_json)["similar_to"]
        r_score = json.loads(new_obj_json)["similarity_score"]
        self.assertEqual(r_id, -1)
        self.assertEqual(r_score, float('-inf'))
        return                                         
                                                
    def test_similarity_score_by_id(self):
        es = self._es
        r_id, _ = text_similarity_score_by_id(index=self._index_name, doc_type=self._doc_type_name, id=0)
        self.assertEqual(r_id, 0 + self._data_size)
        return 
        
    @classmethod
    def tearDownClass(cls):
        cls._es.indices.delete(index = cls._index_name)
        return 
        
if __name__ == '__main__':
    main()
        
