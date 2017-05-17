import logging
from stravalib.client import Client

# Get an instance of a logger
logger = logging.getLogger(__name__)

def get_stravauth_url(approval_prompt="auto", scope="write"):
    from django.conf import settings
    logger.info('get_stravauth_url begging')
    
    client = Client()
    authorize_url = client.authorization_url(client_id=settings.CLIENT_ID, redirect_uri=settings.STRAVA_REDIRECT, 
    approval_prompt=approval_prompt, scope=scope)
    # TODO: check scope and approval_prompt are reasonable 

    return authorize_url
    #return "%s?%s" % (strava_url, vars)