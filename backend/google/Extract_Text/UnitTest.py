__author__ = 'shyu'
from googleapiclient.discovery import build
import checkAlchemy_Tika as ca
import mechanize
import cookielib
from TikaExtractCookieDownloader import DocumentConvertor as dc
from TikaExtractCookie import DocumentConvertor as dcc


failed_url ="http://www.connectedaction.net/wp-content/uploads/NodeXL%20Twitter%20Social%20Network%20Analysis%20Data%20Sets/NodeXL%20-%20Collection%20-%20Twitter%20-%20oracle_2010-08-14_05-15-02.xlsx"

def excel_Test (querystr):
    service = build("customsearch", "v1", developerKey="AIzaSyC8viCWyzR_q2MBKLeRZGpc7BHA3NTNimA")
    collection = service.cse()
    search_engine_id = '012608441591405123751:clhx3wq8jxk'
    start_val = 0


    request = collection.list(
        q=querystr,
        # num=10, #this is the maximum & default anyway
        # start=start_val,
        cx=search_engine_id,
        #fileType=ft
    )


    response = request.execute()

    for i, doc in enumerate(response['items']):
        url = doc.get('link')
        print url
        query1 = dcc(url)
        print query1.parsed_json['content']


def forbidden_test():

    #ca.checkLink('https://utsacloud.sharepoint.com/sites/publicfolders/UTSA%20Forms/UTShare%20PeopleSoft/Crosswalk%20Tools/DEFINE%20Unit%20Code%20to%20PS%20Dept%20ID%20Crosswalk.xlsx')
    q = ca.checkLink('https://www.microsoft.com/en-us/legal')
    print q.parsed_json['content']


def forbidden_test_withMechanize():

    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    #br.add_password('http://safe-site.domain','username','password')
    r = br.retrieve(failed_url)

    print r[0]
    query1 = dc(r[0])
    print query1.parsed_json['content']


forbidden_test()
#forbidden_test_withMechanize()
