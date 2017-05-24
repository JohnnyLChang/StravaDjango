# -*- coding: utf8 -*-
from stravalib.client import Client
from datetime import timedelta
import logging

logging.basicConfig()

client = Client(access_token='f91aebddd4bc9a15e28840703966bb27d11d70f0');

friendDe = 4303495;

for activity in client.get_activities(limit=1):
    strava_id = u'{0.id}'.format(activity)
    print "no calories here"
    print "upload_id:", strava_id
    print "calories:", u'{0.calories}'.format(activity)

print "starred_segments"
starred_segments = client.get_starred_segment()

print "athletes"
me = client.get_athlete()
friend = client.get_athlete(athlete_id=friendDe)

print "list differences"
for segment in starred_segments:
    Deefforts = client.get_segment_efforts(segment.id, athlete_id=friendDe, limit=1)
    #Myefforts = client.get_segment_efforts(segment.id, athlete_id=client.get_athlete().id, limit=1)

    friendrecord = None
    myrecord = None
    for deeffort in Deefforts:
        friendrecord = deeffort
    
    #for myeffort in Myefforts:
        #myrecord = myeffort
    
    if friendrecord and segment.athlete_pr_effort:
        vs = u'輸'
        diff = segment.athlete_pr_effort.elapsed_time - deeffort.elapsed_time
        if segment.athlete_pr_effort.elapsed_time < friendrecord.elapsed_time:
            diff = deeffort.elapsed_time - segment.athlete_pr_effort.elapsed_time
            vs = u'贏'
    
        print "路段", u'{0.name} '.format(segment), u'{0.firstname} {1} {2.firstname} {3}秒'.format(me, vs, friend, diff.seconds)

    #leaderboard = client.get_segment_leaderboard(segment.id, following=True, page=1, top_results_limit=40, context_entries=15)
    #print u"> {0.entry_count} entries".format(leaderboard)
    #print u"> current page size", len(leaderboard.entries)
    #for entry in leaderboard:
    #    print u"> {0.rank}. {0.athlete_id} - {0.athlete_name}".format(entry)