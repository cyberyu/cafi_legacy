from unittest import TestCase, main
from datetime import datetime
import numpy as np
from elasticsearch import Elasticsearch
from sklearn.datasets import fetch_20newsgroups
from elasticsearch.helpers import bulk, scan
from text_util import text_similarity_scores
from time import sleep

def random_sample_by_pct(a,pct):
    """
    randomly pct(<= 1.0)  sample without replacement from the list a
    """
    n = len(a)
    np.random.seed(4)
    idx = np.random.random(n) < pct 
    return [a[i] for i in range(n) if idx[i]]

class TextDuplicationTestCase(TestCase):
    def test_similarity_scores(self):
        """
        test text_util.text_similarity_scores() on a synthetic dataset
        """
        # make some duplicated documents from sklearn/newsgroup data. 
        categories = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']
        twenty_train = fetch_20newsgroups(subset='train',categories=categories, shuffle=True, random_state=42)
        data_size = 100
        sample_pct = 0.9
        new_data = [' '.join(random_sample_by_pct(data.split(" "), sample_pct)) for data in twenty_train.data[:data_size]]
        data_to_insert = new_data + twenty_train.data[:data_size]

        #test whether duplications are identified. 
        es = Elasticsearch()
        actions = []
        for i,data in enumerate(data_to_insert):
            actions.append({'_id':i, '_source':{'data':data}})
        rv = bulk(es,actions,stats_only=True,index = "textsimilaritytest", doc_type="newsgroup",refresh=True) #default action is 'index'
        self.assertEqual(rv[1], 0)  # assert no failure
        rv = es.search(index="textsimilaritytest", doc_type="newsgroup", body={"query":{"match_all":{}}},search_type="count")
        self.assertEqual(rv['hits']['total'], len(data_to_insert))
        rv_mat = text_similarity_scores(index = "textsimilaritytest", doc_type = "newsgroup", mlt_fields=['data'])
        self.assertTrue((np.abs(rv_mat.row-rv_mat.col)==data_size).all())
        es.indices.delete(index = "textsimilaritytest")

if __name__ == '__main__':
    main()
        
