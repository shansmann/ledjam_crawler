# coding=utf-8

import json
import os
import sys
from datetime import datetime
import json, time
import requests
from firebase import firebase

from threading import Thread, current_thread
from flask import Flask, request, __version__, render_template, jsonify

application = Flask(__name__, static_folder='web/static', template_folder='web/templates')
PORT = int(os.getenv('PORT', '8087'))

def get_tracks():

    while True:

        db = firebase.FirebaseApplication('https://ledjam-a27cd.firebaseio.com', None)

        print('starting bot.')
        data = request_data()

        for entry in data['tracks']:

            try:
                s_url = entry['spotify']['url']
            except:
                s_url = ''

            try:
                d_url = entry['deezer']['url']
            except:
                d_url = ''

            post_data(db, entry['artist'], entry['title'], s_url, d_url)

        print('tracks saved.')

        time.sleep(60*20)

def request_data():
    url = 'http://www.djamradio.com/actions/infos.php'

    r  = requests.post(url)

    data = r.text

    data = json.loads(data)

    return data

def post_data(firebase, artist, track, s_url, d_url):
    tmp = {}

    tmp['artist'] = artist
    tmp['track'] = track
    tmp['spotify'] = s_url
    tmp['deezer'] = d_url

    result = firebase.post('/tracks', tmp)

p = Thread(target=get_tracks)
p.start()

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=int(PORT), threaded=True, debug=False)
