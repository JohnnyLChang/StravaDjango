# -*- coding: utf8 -*-
from stravalib.client import Client
from datetime import timedelta
import logging

logging.basicConfig()

client = Client(access_token='f91aebddd4bc9a15e28840703966bb27d11d70f0');

for athlete in client.get_club_members(club_id=232265):
    koms = client.get_athlete_koms(athlete_id=athlete.id)
    for segment in koms:
        print u'{0.lastname 0.firstname}: 路段 {1.name} - {1.elapsed_time} 秒'.format(athlete , segment)

