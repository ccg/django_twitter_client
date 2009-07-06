from datetime import datetime
import zoauth
from urllib2 import HTTPError
from localsettings import CONSUMER_KEY, CONSUMER_SECRET

TWITTER = zoauth.provider.ServiceProvider(
    'Twitter', # Name
    'http://twitter.com/oauth/request_token', # Request Token URL
    'http://twitter.com/oauth/authorize', # User Auth URL
    'http://twitter.com/oauth/access_token', # Access Token URL
    realm='Twitter API', # Realm
)

MY_CONSUMER = TWITTER.Consumer(CONSUMER_KEY, CONSUMER_SECRET)

try:
    request_token = MY_CONSUMER.get_request_token()
    print request_token.user_auth_url()
    raw_input("press enter after authorization...")
    access_token = request_token.get_access_token()
    req = access_token.Request('http://twitter.com/statuses/update.json')
    req.params['status'] = 'TEST ' + str(datetime.now())
    status_code, headers, data = req.send()
    print "status, headers, data:", status_code, headers, data
except HTTPError, e:
    print e
