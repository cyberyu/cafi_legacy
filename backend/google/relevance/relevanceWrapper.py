__author__ = 'shiyu'

import psycopg2
import doc_to_label, db

def main():
    conn_string = "host='localhost' dbname='cafi' user='cafi' password='cafi'"
    conn = psycopg2.connect(conn_string)

    #Define data columns
    tf=["text", "title", "snippet"]

    #Retrieve data
    text_file = db.readDB(conn, textfield = tf)

    print "Prepared Model Ready Data"

    #Apply Classifier and Obtain Ids to be confirmed
    ids_to_confrim = doc_to_label.classify(conn, text_file, textfield = tf)

    #doc_to_label.debug()
