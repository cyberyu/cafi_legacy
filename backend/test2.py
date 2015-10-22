import requests
from tika import parser

s = requests.session()
url = 'http://www.vtk.org/wp-content/uploads/2015/04/file-formats.pdf'
#url = 'http://hdwallpaperspretty.com/wp-content/gallery/beauty-nature-images/24701-nature-natural-beauty.jpg'
#url = 'http://docs.python-requests.org/en/latest/'
url = 'http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests'

import sys
url = sys.argv[1]
r = s.get(url)

txt_fmts = ('text/html', 'text/plain', 'application/xhtml+xml', 'application/xml')
if r.headers.get('content-type').strip() in txt_fmts: 
    print r.content
print r.headers
#print parser.from_buffer(r.content).get('content')
from IPython import embed
#embed()
#with open('t.pdf', 'wb') as f:
#    f.write(r.content)
#f.close()
