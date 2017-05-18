from django.conf import settings
from django.contrib.auth.models import User

from stravauth.models import StravaToken
from stravalib import Client
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class StravaV3Backend(object):
    """
    Authenticate using the Strava V3 API.
    """
    def authenticate(self, code):
        logger.info('StravaV3Backend.authenticate begging')
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET
        
        # Make the request to the API
        client = Client()
        access_token = client.exchange_code_for_token(client_id=client_id, client_secret=client_secret, code=code)
        athlete = client.get_athlete()
        
        # username must be unique hence use id
        username = "%s: %s %s" % (athlete.id , athlete.firstname, athlete.lastname)
        
        # Get or create the user (returns tuple)
        try:
            user = User.objects.get(id=athlete.id)
        except:
            logger.error('User.objects.get failed')
            user = User(id=athlete.id)
        
        # Update username
        logger.info('Update username: '+username)
        user.username = username
        user.save()  
        
        # Add the token 
        (token_model, created) = StravaToken.objects.get_or_create(user=user)
        logger.info('Update token: '+access_token)         
        token_model.token = access_token
        token_model.code = code
        token_model.save()
        
        logger.info(user)
        # Return the user
        return user
        
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            logger.error('user '+user_id+' does not exist')
            return None