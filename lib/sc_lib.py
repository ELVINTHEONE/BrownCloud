import os
import json
from enum import Enum
import soundcloud

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
AUTH_REDIRECT = os.environ['AUTH_REDIRECT']

# request enumeration
class RequestType(Enum):
    friends = 1
    tracks = 2
    playlists = 3
    user_favorites = 4
    user_playlists = 5

# get a generic SoundCloud client that has been authorized using the BrownCloud client secret
def _getGenericClient():
    return soundcloud.Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_url=AUTH_REDIRECT
            )

# jsonify a list
def _toJson(list):
    return json.dumps(list, default=lambda o: o.__dict__)

# send a request to SoundCloud
def _sendQuery(request, type, limit):
    # spawn a generic client
    client = _getGenericClient()
    ret = None
    if (type == RequestType.friends):
        query = request.json['query']
        ret = client.get(
            '/users',
            q = query,
            limit = limit
        )
    elif (type == RequestType.tracks):
        query = request.json['query']
        ret = client.get(
            '/tracks',
            q = query,
            tags = request.json['tags'],
            filter = request.json['visibility'],
            #license = request.json['license'],
            bpmFrom= request.json['bpmFrom'],
            bpmTo = request.json['bpmTo'],
            durationFrom = request.json['durationFrom'],
            durationTo = request.json['durationTo'],
            createdAtFrom = request.json['createdAtFrom'],
            createdAtTo = request.json['createdAtTo'],
            genres = request.json['genres'],
            types = request.json['type'],
            limit = limit
        )
    elif (type == RequestType.playlists):
        query = request.json['query']
        ret = client.get(
            '/playlists',
            q = query,
            limit = limit
        )
    elif (type == RequestType.user_favorites):
        ret = client.get('/users/' + request.json['user_id'] + '/favorites')
    elif (type == RequestType.user_playlists):
        ret = client.get('/users/' + request.json['user_id'] + '/playlists')

    return _toJson(ret)
