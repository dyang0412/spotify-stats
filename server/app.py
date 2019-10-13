''' Example of Spotify client credentials flow.
User can search artist names available in Spotify.
Basic flow:
    Get authorization -> get access token -> access endpoints with token
Note:
    Used in server-to-server authentication. Only can access endpoints
    that do not serve user data. Advantage of this flow over API requests
    without an access token is a higher rate limit.
Required environment variables:
    FLASK_APP, CLIENT_ID, CLIENT_SECRET, SECRET_KEY
More info:
    https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
'''


from flask import abort, Flask, redirect, render_template, request, session, url_for, jsonify
from flask_cors import CORS, cross_origin
from flask_session import Session
import json
import logging
import os
import requests


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG
)


# Client info
CLIENT_ID = 'e55da797b0c147918d46e9249268d617'
CLIENT_SECRET = 'e772350d49134d6e86309bfa4b289fe1'

# Spotify API endpoints
TOKEN_URL = 'https://accounts.spotify.com/api/token'
SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'
TRACK_ANAL_ENDPOINT = 'https://api.spotify.com/v1/audio-analysis'
TRACK_FEATURES_ENDPOINT = 'https://api.spotify.com/v1/audio-features'
ALBUM_ENDPOINT = 'https://api.spotify.com/v1/albums'
ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists'
# Start 'er up
app = Flask(__name__)
SECRET_KEY = "changeme"
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/auth', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def auth():
    if request.method == 'GET':
        '''Get user authorization and set access token.'''
        # Request authorization from user
        payload = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'grant_type': 'client_credentials',
        }

        # `auth=(CLIENT_ID, SECRET)` basically wraps an 'Authorization'
        # header with value:
        # b'Basic ' + b64encode((CLIENT_ID + ':' + SECRET).encode())
        res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)
        res_data = res.json()
        access_token = res_data.get('access_token')

        if not access_token or res.status_code != 200:
            abort(400)
        else:
            session['access_token'] = access_token   
            print('Access Token: ' + session.get('access_token'))

    response = jsonify({'access_token': access_token})

    return response



def _query_search(trackname=None, token=None):
    '''Make request for data on `artist`.'''

    if trackname is None:
        return trackname

    print(session.get('access_token'))
    payload = {'q': trackname, 'type': 'track', 'limit': '20'}
    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    return requests.get(SEARCH_ENDPOINT, params=payload, headers=headers)


def _query_trackAnal(trackid=None, token=None):
    if trackid is None:
        return trackid

    print(session.get('access_token'))
    payload = trackid
    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    return requests.get(TRACK_ANAL_ENDPOINT+'/'+payload, headers=headers)

def _query_trackFeatures(trackid=None, token=None):
    if trackid is None:
        return trackid

    print(session.get('access_token'))
    payload = trackid
    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    return requests.get(TRACK_FEATURES_ENDPOINT+'/'+payload, headers=headers)

def _query_album(albumid=None, token=None):
    if albumid is None:
        return albumid

    print(session.get('access_token'))
    payload = albumid
    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    return requests.get(ALBUM_ENDPOINT+'/'+payload, headers=headers)

def _query_artist(artistid=None, token=None):
    if artistid is None:
        return artistid

    print(session.get('access_token'))
    payload = artistid
    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    return requests.get(ARTIST_ENDPOINT+'/'+payload, headers=headers)


@app.route('/search', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def search():
    '''Simple example search for a track.'''
    if request.method == 'POST':
        data = request.get_json()
        trackname = data.get('trackname')
        token = data.get('token')
        #artist = request.form.get('artist')
        if trackname:
            res = _query_search(trackname,token)
            res_data = res.json()

            if res_data.get('error') or res.status_code != 200:
                
                abort(400)
            else:
                #print(json.dumps(res_data))
                return res_data

        else:
            abort(400)


@app.route('/get-trackAnal', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def getTrack():
    if request.method == 'POST':
        data = request.get_json()
        trackID = data.get('trackID')
        token = data.get('token')
        #artist = request.form.get('artist')
        if trackID:
            res = _query_trackAnal(trackID,token)
            res_data = res.json()
            if res_data.get('error') or res.status_code != 200:
                abort(400)
            else:
                #print(json.dumps(res_data))
                return res_data
        else:
            abort(400)


@app.route('/get-trackFeatures', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def getTrackFeatures():
    if request.method == 'POST':
        data = request.get_json()
        trackID = data.get('trackID')
        token = data.get('token')
        #artist = request.form.get('artist')
        if trackID:
            res = _query_trackFeatures(trackID,token)
            res_data = res.json()
            if res_data.get('error') or res.status_code != 200:
                abort(400)
            else:
                #print(json.dumps(res_data))
                return res_data
        else:
            abort(400)

@app.route('/get-album', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def getAlbum():
    if request.method == 'POST':
        data = request.get_json()
        albumID = data.get('albumID')
        token = data.get('token')
        #artist = request.form.get('artist')
        if albumID:
            res = _query_album(albumID,token)
            res_data = res.json()
            if res_data.get('error') or res.status_code != 200:
                abort(400)
            else:
                #print(json.dumps(res_data))
                return res_data
        else:
            abort(400)

@app.route('/get-artist', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def getArtist():
    '''Simple example search for a track.'''
    if request.method == 'POST':
        data = request.get_json()
        artistID = data.get('artistID')
        token = data.get('token')
        #artist = request.form.get('artist')
        if artistID:
            res = _query_artist(artistID,token)
            res_data = res.json()
            if res_data.get('error') or res.status_code != 200:
                abort(400)
            else:
                #print(json.dumps(res_data))
                return res_data
        else:
            abort(400)

BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

if __name__ == '__main__':
    app.run()