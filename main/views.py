# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_twitter_oauth_test.main.forms import TwitterForm
from django.http import HttpResponse, HttpResponseRedirect
from twitter_app.utils import *
import twitter_app.oauth as oauth
# FIXME refactor this http-connection stuff
import httplib
import logging

CONSUMER = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)

@login_required
def index(request):
    if request.method == "POST":
        form = TwitterForm(request.POST)
        if form.is_valid():
            tweet = request.POST.get('tweet', '')
            tweetlen = len(tweet)
            if tweetlen < 1 or tweetlen > 140:
                logging.error("Tweet-length validation failed!")
                logging.error("Tweet: '%s'" % tweet)
                logging.error("Length: %d" % tweetlen)
                return HttpResponse("TwitterForm validation failed!"
                                    " Check logs.")
            # TODO send tweet here.
            logging.debug("tweet='%s'" % tweet)
            # Submitted form was processed, so create a new, blank one.
            form = TwitterForm()
        else:
            logging.debug("got invalid form")
    else:
        form = TwitterForm()
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
