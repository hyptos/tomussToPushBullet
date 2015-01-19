#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Antoine'

import json
import datetime
import requests
from bs4 import BeautifulSoup


def remSecs(tm, secs):
    """Returns a date tm with secs removed."""

    fulldate = datetime.datetime(
        tm.year,
        tm.month,
        tm.day,
        tm.hour,
        tm.minute,
        tm.second,
    )
    fulldate = fulldate - datetime.timedelta(seconds=secs)
    return fulldate


def sendNotificationToPushBullet(str):
    """Send a notification to PushBullet with str as the body."""

    token = 'SUPER_TOKEN'
    payload = {'type': 'note', 'title': 'FAC nouvelle note',
               'body': str}
    headers = {'content-type': 'application/json'}
    p = requests.post('https://api.pushbullet.com/v2/pushes',
                      data=json.dumps(payload), headers=headers,
                      auth=(token, ''))
    if p.status_code == 200:
        print 'Success'
    else:
        print p.json
        print 'Notification failed'


r = requests.get('https://tomusss.univ-lyon1.fr/2014/Automne/rss/f10447ae7785342')
if r.status_code == 200:
    soup = BeautifulSoup(r.text)
    items = soup.findAll('item')
    now = datetime.datetime.now()
    last5min = remSecs(now, 300)
    for it in items:
        if it.title.text.split(':')[2]:
            matiere = it.title.text.split(':')[1].strip()
            projet = it.title.text.split(':')[0].strip()
            note = it.title.text.split(':')[2].strip()
            pubdate = it.pubdate.text
            pubdate = now.strptime(pubdate,
                                   '%a, %d %b %Y %H:%M:%S +0000')
            isNote = note.split('/')

            if len(isNote) >= 2:
                if pubdate >= last5min:
                    content = note + ' en ' + projet + ' pour ' \
                              + matiere + ' le ' \
                              + pubdate.strftime('%d/%m/%Y a %H:%M:%S')
                    sendNotificationToPushBullet(content)

