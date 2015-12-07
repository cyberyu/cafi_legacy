# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:23:40 2015

@author: Kun Shi,  Shi Yu


"""
import numpy as np
import StringIO
import os
import sys
import shutil
import logging


_DBTABLE_ = 'google_searchresult'
_DBFIELDS_ = ['id', 'tile', 'snippet', 'text', 'relevance', 'predicted_relevance', 'predicted_score']
_RELEVANCE_LABEL_POS_ = 'y'
_RELEVANCE_LABEL_NEG_ = 'n'


#__package__="CAFI.activelearning"

def remove_control_characters(s):
    """
    Remove the control characters from the string.

    @type  s:  python string object
    @param s:  the string where control characters need to be removed

    @return: string without control characters
    """

    #return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")
    return ''.join([i if 31 < ord(i) <127 else ' ' for i in s])



def readDB(conn, **kwargs):
    """
    Return the textual Google Search Results data for feature engineering in Relevance Filtering.

    @type  conn:  psycopg2 connection object
    @param conn:  The established connection object to the Google Search Result database

    @param kwargs:   remaining keyword arguments are passed to readDB functon, see below

    Args:
    @type textfield:  list object
    @param textfield: the list of Google Search Result table names to be concatenated as text field. Example: ['fulltext', 'srtitle']

    @type training_srids: list object
    @param training_srids: the list of document ids used as training data

    @type test_srids: list object
    @param test_srids: the list of document ids used as test data

    @returns: A python dictionary {"docs": docs, "labels": label, "srids":srids}.  Docs are a list of text.  Labels are a list of relevance flags used for training.  srids is a list of document ids.
    """

    logging.info('prepare to read database')     

    # conn.cursor will return a cursor object, you can use this cursor to perform querie
    cursor = conn.cursor()

    # reading the input parameters
    textfield = kwargs.pop('textfield','fulltext')


    # try to get the training and test document ids
    training_srids = kwargs.pop('training_srids',None)
    test_srids = kwargs.pop('test_srids',None)


    logging.debug('user input textfields are: ' + ','.join(textfield))  
    if(training_srids is not None):
        logging.debug('user input training doc Ids are: ', ','.join(training_srids))
    if(test_srids is not None):        
        logging.debug('user input test doc Ids are: ', ','.join(test_srids))
    

    # get the unique value, and ordered in alphabetical order
    textfield_set = frozenset(textfield)

    # construct the query terms from title, snippet, or fulltext
    #intersection = [x for x in ['srtitle', 'srsnippet', 'srtext'] if x in textfield_set]
    intersection = [x for x in [_DBFIELDS_[1], _DBFIELDS_[2], _DBFIELDS_[3]] if x in textfield_set]
    
    logging.info('query database fieldnames: ' + ','.join(intersection))

    # execute our Query & retrieve the records from the database

    # Construct the Training Data Set
    #cursor.execute("""SELECT "relevanceFlag" FROM "tblSearchResults" ORDER BY "srId" """)
    if ((training_srids is not None) and (test_srids is not None)):

        data_Query = "SELECT %s, %s, %s " \
                     "FROM %s " \
                     "where %s in %s " \
                     "UNION " \
                     "SELECT NULL, %s, %s " \
                     "FROM %s " \
                     "Where %s in %s ORDER BY %s "\
                     % (_DBFIELDS_[4], _DBFIELDS_[0], ','.join(intersection),
                        _DBTABLE_,
                        _DBFIELDS_[0], repr(tuple(map(str,training_srids))),
                        _DBFIELDS_[0], ','.join(intersection),
                        _DBTABLE_,
                        _DBFIELDS_[0], repr(tuple(map(str,test_srids))), _DBFIELDS_[0]
                        )                        

    elif ((training_srids is not None) and (test_srids is None)):
        # if the training srid list is avaliable, but test_srids is empty.
        # By default, get all the training_srids records as training data, then all other records whose relevance flags are missing as test data
        #
                        
        data_Query = "SELECT %s, %s, %s " \
                     "FROM %s " \
                     "where %s in %s AND (%s is not NULL) " \
                     "UNION " \
                     "SELECT NULL, %s, %s " \
                     "FROM %s " \
                     "where %s is null ORDER BY %s "\
                     % (_DBFIELDS_[4], _DBFIELDS_[0], ','.join(intersection),
                        _DBTABLE_,
                        _DBFIELDS_[0], repr(tuple(map(str,training_srids))), _DBFIELDS_[4],
                        _DBFIELDS_[0], ','.join(intersection),
                        _DBTABLE_,
                        _DBFIELDS_[4], _DBFIELDS_[0]
                        )                        

    elif ((training_srids is None) and (test_srids is not None)):
                        
        data_Query = "SELECT %s, %s, %s " \
                     "FROM %s " \
                     "where (%s is not NUll) AND (%s not in %s) " \
                     "UNION " \
                     "SELECT NULL, %s, %s" \
                     "FROM %s " \
                     "where %s is null AND (%s in %s) ORDER BY %s "\
                     % (_DBFIELDS_[4], _DBFIELDS_[0], ','.join(intersection),
                        _DBTABLE_,
                        _DBFIELDS_[4], _DBFIELDS_[0], repr(tuple(map(str,test_srids))),
                        _DBFIELDS_[0], ','.join(intersection),
                        _DBTABLE_,
                        _DBFIELDS_[4], _DBFIELDS_[0], repr(tuple(map(str,test_srids))), _DBFIELDS_[0]
                        )                        


    elif ((training_srids is None) and (test_srids is None)):

        data_Query = "SELECT %s, %s, %s " \
                     "FROM %s " \
                     "where %s is not NUll " \
                     "UNION " \
                     "SELECT NULL, %s, %s " \
                     "FROM %s " \
                     "where %s is NULL ORDER BY %s "\
                     % (_DBFIELDS_[4], _DBFIELDS_[0], ','.join(intersection),
                        _DBTABLE_,
                        _DBFIELDS_[4],
                        _DBFIELDS_[0], ','.join(intersection),
                        _DBTABLE_,
                        _DBFIELDS_[4], _DBFIELDS_[0]
                        )                       

   
    logging.info('start to read the data base')    
    logging.debug('data query is: %s', data_Query)    
    
    
    # excute data_Query
    try:   
        cursor.execute(data_Query)
    except Exception:
        logging.error('Failed to excute data query', exc_info=True)
    logging.info('finish reading the database')    

    # fetch records
    records = cursor.fetchall()

    logging.info('total number of records read from database is: %s', len(records))
    #logging.debug('records are: %s', records)    


    # get all the labels for the records
    label = [item[0] for item in records]
    label = np.array(label)

    # get all the ids for the records, the srids should be one-to-one mapped to the training data
    srids = [item[1] for item in records]
    docs = [" ".join(filter(None,item[2:])) for item in records]


    #fd = open('/home/shiyu/temp.txt','w')
    #fd.write(str(docs))
    #fd.close()

    # close cursor
    cursor.close()

    # returns
    return({"docs": docs, "labels": label, "srids":srids})


def updateDB(conn, **kwargs):
    """
    Update the Google Search Results table after the test data has been predicted with relevance labels and relevance scores.

    @type  conn:  psycopg2 connection object
    @param conn:  The established connection object to the Google Search Result database

    @param kwargs:   remaining keyword arguments are passed to readDB functon, see below

    Args:
    @type idlist:  list object
    @param idlist: the list of document ids whoses labels or relevance scores need to be updated.

    @type type: string object
    @param type: the type of values to be updated. If type='label', then update the relevance flags of the documents. \
    If type='relevanceScore', then update the relevance scores of the documents

    @type value: list object
    @param value: the list of values need to be updated

    @returns: null
    """

    # get the recommended or test ids
    idlist = kwargs.pop('idlist',None)
    value = kwargs.pop('value',None)
    type = kwargs.pop('type', None)

    logging.info('prepare to update database column of %s with %s ids and %s values', 'predictionLabel' if type is 'label' else type, len(idlist), len(value)) 
    if(idlist is not None):
        logging.debug('record ids to be updated are: ' + ','.join(map(str,idlist)))
    if(value is not None):
        logging.debug('record values to be updated are: ' + ','.join(map(str,value)))
    
    if ((idlist is not None) and (value is not None) and (len(idlist)==len(value))) :

        logging.info('start to update %s in database', 'predictionLabel' if type is 'label' else type)
        
        cursor = conn.cursor()
        if (type=='label'):
            # reset to NULL before update
            cursor.execute("UPDATE %s set %s=NULL WHERE %s is not NULL" %(_DBTABLE_, _DBFIELDS_[5], _DBFIELDS_[5]))
            cursor.executemany("UPDATE %s set %s=%s WHERE %s=%s" %(_DBTABLE_, _DBFIELDS_[5], '%s', _DBFIELDS_[0], '%s'), zip(value, idlist))
        elif (type=='relevanceScore'):
            #cursor.execute("UPDATE tblsearchresults set sqrelevancescore=NULL WHERE sqrelevanceScore is not NULL")
            #cursor.executemany("UPDATE tblsearchresults set sqrelevancescore=%s WHERE srid=%s", zip(value, idlist))
            cursor.execute("UPDATE %s set %s=NULL WHERE %s is not NULL" %(_DBTABLE_, _DBFIELDS_[6], _DBFIELDS_[6]))
            cursor.executemany("UPDATE %s set %s=%s WHERE %s=%s" %(_DBTABLE_, _DBFIELDS_[6], '%s', _DBFIELDS_[0], '%s'), zip(value, idlist))
        elif (type=='relevanceFlag'):
            #cursor.executemany("UPDATE tblsearchresults set relevanceflag=%s WHERE srid=%s", zip(value, idlist))
            cursor.executemany("UPDATE %s set %s=%s WHERE %s=%s" %(_DBTABLE_, _DBFIELDS_[4], '%s', _DBFIELDS_[0], '%s'), zip(value, idlist))
        conn.commit()
        cursor.close()
        logging.info('finish updating %s with %s records in database', type, len(value))                        

    else:
        logging.warning('Not update database due to either unmatched length or zero length of id & value')


def ingestDB(conn, dir, label, **kwargs):
    """
    Ingest sample data to the Google Search Results table.

    @type  conn:  psycopg2 connection object
    @param conn:  The established connection object to the Google Search Result database

    @type dir:  string
    @param dir: the root directory of textual files to be ingested to the table


    @type label: integer 0 or 1
    @param label: the relevance flag of all the textual files being ingested to the data table

    @returns: null
    """
  
    logging.info('start to ingest data to database')    

    curs = conn.cursor()

    try:
        
        data_Query = "CREATE TABLE IF NOT EXISTS %s (%s varchar NOT NULL, "\
                     "%s varchar NULL," \
                     "%s varchar NULL," \
                     "%s Text NULL," \
                     "%s Integer NULL," \
                     "%s Integer NULL," \
                     "%s float NULL" \
                     ")" \
                     % (_DBTABLE_, _DBFIELDS_[0],
                        _DBFIELDS_[1],
                        _DBFIELDS_[2],
                        _DBFIELDS_[3],
                        _DBFIELDS_[4],
                        _DBFIELDS_[5],
                        _DBFIELDS_[6]                        
                        )
        
        logging.info('start creating table %s with field names of %s,%s,%s,%s,%s,%s,%s ', _DBTABLE_, _DBFIELDS_[0],
                     _DBFIELDS_[1],_DBFIELDS_[2],_DBFIELDS_[3],_DBFIELDS_[4],_DBFIELDS_[5],_DBFIELDS_[6])
        logging.debug('data query is: %s', data_Query)
             
        
        try:                
            curs.execute(data_Query)        
        except Exception:
            logging.error('Failed to create table', exc_info=True)

        logging.info('finish creating table')

    except:
        conn
    conn.commit()


    logging.info('start to copy data to table')
    try:
        # construct a buffered StringIO
        data = StringIO.StringIO()

        for subdir, dirs, files in os.walk(dir):
            for file in files:
                filepath = subdir+os.sep+file

                # remove some characters that are harmful to break the code '\.'
                text = open(filepath,'r').read().replace('|',' ').replace('\.',' ').replace('\n',' ')

                id = os.path.splitext(os.path.basename(file))[0]

                vt = '|'.join([id,'','',text,label,'',''])

                # remove control characters
                vt = remove_control_characters(vt)

                data.write(vt.replace('\t',' ').replace('\n', ' ')+'\n')

        data.seek(0)
        #logging.debug('construct buffered StringIO data: %s', data.getvalue())

        # use this if want to save the file and check
        # fd = open('/home/shiyu/temp.txt','w')
        # shutil.copyfileobj(data,fd)
        # fd.close()


    except Exception:
        logging.error('Failed to construct buffered stringIO', exc_info=True)

    # optional, instead of copy from buffered object, also can copy from saved file
    # fd = open('/home/shiyu/temp.txt','r')
    #curs.copy_from(fd,'tblSearchResults', sep='|', null='')

    curs.copy_from(data,_DBTABLE_, sep='|', null='')
    conn.commit()

    logging.info('finish to copy data to table') 

