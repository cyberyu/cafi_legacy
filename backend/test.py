from dragnet import content_extractor, content_comments_extractor
import requests
import sys
from IPython import embed

r = requests.get(sys.argv[1])

c = content_extractor.analyze(r.content, blocks=True)
print '\n\n'.join(b.text for b in c)

print '\n\n-------------\n\n'

c = content_comments_extractor.analyze(r.content, blocks=True)
print '\n\n'.join(b.text for b in c)
#print c

