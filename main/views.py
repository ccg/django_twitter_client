# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_twitter_oauth_test.main.forms import TwitterForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError

from twitter_app.utils import *
import twitter_app.oauth as oauth

# FIXME refactor this http-connection stuff
import httplib
import simplejson
import StringIO
import pprint
import logging

CONSUMER = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)

@login_required
def index(request):
    profile = request.user.get_profile()
    if not profile.can_tweet():
        return render_to_response('main/index.html', locals(),
                                  context_instance=RequestContext(request))
    access_token_string = profile.oauth_token
    access_token = oauth.OAuthToken.from_string(access_token_string)
    conn = httplib.HTTPSConnection(SERVER)
    if request.method == "POST":
        form = TwitterForm(request.POST)
        if form.is_valid():
            tweet = request.POST.get('tweet', '')
            logging.debug("tweet='%s'" % tweet)

            json = update_status(CONSUMER, conn, access_token, tweet)

            logging.debug("update_status JSON response: '%s'" % json)
            update_response = simplejson.loads(json)

            # Submitted form was processed, so create a new, blank one.
            form = TwitterForm()
        else:
            logging.debug("got invalid form")
    else:
        form = TwitterForm()
    timeline_json = friends_timeline(CONSUMER, conn, access_token)
    timeline = simplejson.loads(timeline_json)
    if timeline and len(timeline) > 0:
        output = StringIO.StringIO()
        pp = pprint.PrettyPrinter(stream=output, indent=2)
        pp.pprint(timeline[0])
        logging.debug("timeline:")
        logging.debug(output.getvalue())
        output.close()
    conn.close()
    return render_to_response('main/index.html',
                              locals(),
                              context_instance=RequestContext(request),
                              )

@login_required
def return_(request):
    conn = httplib.HTTPSConnection(SERVER)
    unauthed_token = request.session.get('unauthed_token', None)
    if not unauthed_token:
        return HttpResponse("No un-authed token cookie")
    token = oauth.OAuthToken.from_string(unauthed_token)
    if token.key != request.GET.get('oauth_token', 'no-token'):
        return HttpResponse("Something went wrong! Tokens do not match")
    access_token = exchange_request_token_for_access_token(CONSUMER,
                                                           conn,
                                                           token)
    profile = request.user.get_profile()
    profile.oauth_token = access_token.to_string()
    profile.save()
    conn.close()
    return HttpResponseRedirect('/')
