import json
import requests
from firebase import firebase

def request_data():
    url = 'http://www.djamradio.com/actions/infos.php'

    r  = requests.post(url)

    data = r.text

    data = json.loads(data)

    return data

def post_data(artist, track, s_url, d_url):
    tmp = {}

    tmp['artist'] = artist
    tmp['track'] = track
    tmp['spotify'] = s_url
    tmp['deezer'] = d_url

    result = firebase.post('/tracks', tmp)

if __name__ == '__main__':
    data = request_data()
    firebase = firebase.FirebaseApplication('https://ledjam-a27cd.firebaseio.com', None)

    for entry in data['tracks']:

        try:
            s_url = entry['spotify']['url']
        except:
            s_url = ''
            
        try:
            d_url = entry['deezer']['url']
        except:
            d_url = ''

        post_data(entry['artist'], entry['title'], s_url, d_url)
