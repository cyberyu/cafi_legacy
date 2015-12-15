from tika import parser
from django.conf import settings
import requests
from urllib2 import urlparse
import os
import uuid
from dragnet import content_comments_extractor

import logging
logger = logging.getLogger("CAFI")

txt_fmts = ('text/html', 'text/plain', 'application/xhtml+xml', 'application/xml')

def get_name_from_url(url):
    o = urlparse.urlsplit(url)
    return os.path.split(o.path)[-1]

def save_file(content, url):
    filename = get_name_from_url(url)
    filename = "%s-%s" %(str(uuid.uuid4())[:8], filename)
    file_path = os.path.join(settings.DOWNLOAD_DIR, filename)
    with open(file_path, 'wb') as f:
        f.write(content)

    return file_path

def extract_from_file(s):
    data = parser.from_buffer(s, serverEndpoint=settings.TIKA_SERVER)

    return data.get('content')

def extract_from_html(html):
    blocks = content_comments_extractor.analyze(html, blocks=True)

    return '\n'.join([b.text for b in blocks])

def download(url):
    s = requests.session()
    agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
    s.headers.update({'User-agent': agent})
    # `mount` a custom adapter that retries failed connections for HTTP and HTTPS requests.
    s.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))
    s.mount("https://", requests.adapters.HTTPAdapter(max_retries=3))
    r = s.get(url)

    if r.headers.get('content-type', '').split(';')[0].strip() in txt_fmts:
        path = None
        text = extract_from_html(r.content)
        raw_html = r.content
        doc_type = 'txt'
    else:
        path = save_file(r.content, url)
        text = extract_from_file(r.content)
        raw_html = None
        tmp = url.split('.')
        #TODO: find more appropriate way to determine doc type
        if len(tmp) >= 2 and len(tmp[-1])<20: #Checks models.py limit set to 20 for doc_type
            doc_type = tmp[-1]
        else:
            logger.debug(tmp)
            doc_type = ''

    data = {'path': path, 'doc_type': doc_type, 'text': text, 'raw_html': raw_html}

    return data


if __name__ == '__main__':
    import os, sys
    PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../backend')
    sys.path.append(PROJECT_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    # url = 'http://www.vtk.org/wp-content/uploads/2015/04/file-formats.pdf'
    # url = 'http://hdwallpaperspretty.com/wp-content/gallery/beauty-nature-images/24701-nature-natural-beauty.jpg'
    #url = 'http://docs.python-requests.org/en/latest/'
    url = 'http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests'

    print download(url)