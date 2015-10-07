__author__ = 'tanmoy'

from os import path
import re
import urllib2
import unicodedata
import mechanize
from urlparse import urlsplit
import cookielib

#==========================================
browser = mechanize.Browser()   #Reference taken from Shi Yu' code and discussion
cj = cookielib.LWPCookieJar()
browser.set_cookiejar(cj)
browser.set_handle_equiv(True)
#browser.set_handle_gzip(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#browser.set_debug_http(True)
#browser.set_debug_redirects(True)
#browser.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#=============================================

TIMEOUT=30.0

def get_headers(url): #Get the headers

    r = browser.open(url,timeout=TIMEOUT)
    return r.info()

def filename_from_header(header):

    try:
        cd = header['Content-Disposition']
        pattern = 'attachment; filename="(.*?)"'
        m = re.search(pattern, cd)
        g = m.group(1)
        return sanitise_filename(g)
    except Exception:
        return ''

def filename_from_url(url):

    u = urlsplit(url) # parse the url into its components
    parts = [urllib2.unquote(x).strip() for x in u.path.split('/')] # split the path into parts and unquote
    fname = parts[-1] # take the last component as filename

    # if empty, url ended with a trailing slash so join up the hostname/path  and use that as a filename
    if len(fname) < 1:
        s = u.netloc + u.path[:-1]
        fname = s.replace('/','_')
    else:
        # unquoting could have cuased slashes to appear again, split and take the last element
        fname = fname.split('/')[-1]

    # add an extension if none
    ext = path.splitext(fname)[1]
    if len(ext) < 1 or len(ext) > 5: fname += ".html"

    return sanitise_filename(fname)

def sanitise_filename(fileName):
    # ensure a clean, valid filename (arg may be both str and unicode), ensure a unicode string, problematic ascii chars will get removed

    if isinstance(fileName,str):
        fn = unicode(fileName,errors='ignore')
    else:
        fn = fileName

    fn = unicodedata.normalize('NFKD',fn)   # normalize it
    s = fn.encode('ascii','ignore') # encode it into ascii, again ignoring problematic chars
    s = re.sub('[^\w\-\(\)\[\]\., ]','',s).strip() # remove any characters not in the whitelist


    max = 250   # ensure limiting maximum
    fn,ext = path.splitext(s) # split off extension, trim, and re-add the extension
    s = fn[:max-len(ext)] + ext
    return s


#Download a file given a URL. This function downloads a file using the given url.
def download(url, target_dir=".", target_fname=None):


        headers = get_headers(url)# get the headers
        clen = int(headers.get('Content-Length',-1))# get the content length (if present)

        # build the absolute path we are going to write to
        fname = target_fname or filename_from_header(headers) or filename_from_url(url)

        # split off the extension
        _,ext = path.splitext(fname)
        filepath = path.join(target_dir,fname)

        dl = True
        if path.exists(filepath):
            if clen > 0:
                fs = path.getsize(filepath)
                delta = clen - fs
                # all we know is that the current filesize may be shorter than it should be and the content length may be incorrect
                # overwrite the file if the reported content length is bigger than what we have already by at least k bytes (arbitrary)
                # Still not fullproof as the fundamental problem is that the contentlength cannot be trusted

                if delta > 2:
                    print '    - "%s" seems incomplete, downloading again' % fname
                else:
                    print '    - "%s" already exists, skipping' % fname
                    dl = False
            else:
                # missing or invalid content length, assume all is ok...
                dl = False

            return filepath

        try:
           if dl:
               browser.retrieve(url,filepath,timeout=TIMEOUT)
               return filepath

        except Exception as e:
            print "Failed to download url %s to %s: %s" % (url,filepath,e)
            return None

if __name__ == "__main__":
    #Testcases
    url = "http://www.shareholder.com/visitors/activeedgardoc.cfm?f=xls&companyid=AAPL&id=10944291"
    target_dir = "./data/"
    download(url,target_dir,target_fname=None)