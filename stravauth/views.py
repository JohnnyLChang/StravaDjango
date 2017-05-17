from django.conf import settings
from django.contrib.auth import login, authenticate as strava_authenticate
from django import http
from django.shortcuts import redirect
from django.views import generic
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class StravaRedirect(generic.RedirectView):
    """
        Redirects to the Strava oauth page
    """
    def get_redirect_url(self, approval_prompt="auto", scope="write", *args, **kwargs):
        from stravauth.utils import get_stravauth_url
        logger.info("get_redirect_url")
        return get_stravauth_url(approval_prompt, scope)


class StravaAuth(generic.View):
    url = None # Or default?

    def get(self, request, *args, **kwargs):
        code = request.GET.get("code", None)
        logger.info(code)
        if not code:
            # Redirect to the strava url
            logger.info("StravaAuth get_redirect_url")
            view = StravaRedirect.as_view()
            return view(request, *args, **kwargs)
        
        # Log the user in
        logger.info("before strava_authenticate")
        user = strava_authenticate(code=code)
        logger.info("after strava_authenticate")
        logger.info(request)
        logger.info(user)
        login(request, user)
                    
        return http.HttpResponseRedirect(self.url)
        
    