from django.conf import settings
from django.contrib.auth import login, authenticate as strava_authenticate
from django import http
from django.shortcuts import redirect
from django.views import generic
from django.template import loader
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from stravauth.models import StravaToken
from stravalib import Client
from django.conf import settings
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class StravaRedirect(generic.RedirectView):
    def get_redirect_url(self, approval_prompt="auto", scope="write", *args, **kwargs):
        from stravauth.utils import get_stravauth_url
        logger.info("get_stravauth_url")
        return get_stravauth_url(approval_prompt, scope)


class StravaAuth(generic.View):
    url = None # Or default?

    def get(self, request, *args, **kwargs):
        logger.info("StravaAuth")
        code = request.GET.get("code", None)
        logger.info(code)
        if not code:
            # Redirect to the strava url
            logger.info("redirect to strava url")
            view = StravaRedirect.as_view()
            return view(request, *args, **kwargs)
        
        # Log the user in
        logger.info("before strava_authenticate, code="+code)
        user = strava_authenticate(code=code)
        logger.info(user)
        logger.info(request)
        login(request, user)
                    
        return http.HttpResponseRedirect(self.url)

class StravaAthelete(generic.View):
    def get(self, request, athlete_id):
        if request.user.is_authenticated():
            template = loader.get_template('athlete.html')
            try:
                token = StravaToken.objects.get(user=request.user.id)
            except ObjectDoesNotExist:
                logger.error("Either the entry or blog doesn't exist.")
            client_id = settings.CLIENT_ID
            client_secret = settings.CLIENT_SECRET
            client = Client(access_token=token.token)
            logger.info(token.user)
            logger.info(token.token) 
            athlete = client.get_athlete()
            logger.info(athlete.city)
            activities = client.get_activities(limit=10)
            for activity in activities:
                logger.info(u"{0.name} {0.moving_time} {0.suffer_score}".format(activity))
            context = {
            #        'latest_question_list': latest_question_list,
            }
            return HttpResponse(template.render(context, request))
        else:
            raise Http404("user is not login.")