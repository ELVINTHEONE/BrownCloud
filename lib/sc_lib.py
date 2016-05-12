import os
import json
from enum import Enum
import soundcloud

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
AUTH_REDIRECT = os.environ['AUTH_REDIRECT']

DEFAULT_AVI_URL = 'http://a1.sndcdn.com/images/default_avatar_large.png?1462806539'

# request enumeration
class RequestType(Enum):
    friends = 1
    tracks = 2
    playlists = 3
    user_favorites = 4
    user_playlists = 5

# get a generic SoundCloud client that has been authorized using the BrownCloud client secret
def getGenericClient():
    return soundcloud.Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_url=AUTH_REDIRECT
            )

# jsonify a list
def toJson(list):
    return json.dumps(list, default=lambda o: o.__dict__)

# returns true if the given user has an avatar
def _hasAvi(user):
    return user.avatar_url != 'http://a1.sndcdn.com/images/default_avatar_large.png?1462881391'

# add the user, check if 'avatar-only' is true, if so, then make sure the user has an avatar
def _addUser(ret, user, aviOnly):
    if not aviOnly or _hasAvi(user):
        ret.append(user)

# process the users returned from SoundCloud
def getUsers(users, numToFetch, aviOnly, city, country):
    if len(users) <= numToFetch:
        # return the users
        return users
    elif numToFetch > 0:
        # match the users to each of the criteria, rate them based on number matched
        matches = dict({
            0: [], 1: [], 2: []
        })
        maxMatches = 3
        ret = []
        for user in users:
            matchCount = 0
            if user.avatar_url != DEFAULT_AVI_URL:
                matchCount += 1
            if user.city == city:
                matchCount += 1
            if user.country == country:
                matchCount += 1
            if matchCount == maxMatches:
                # add the user to the array directly
                _addUser(ret, match, aviOnly)
                if len(ret) >= numToFetch:
                    break
            else:
                # add the user to the dictionary
                matches[matchCount].append(user)
        # add from each subsequent level of the array
        matchesIx = maxMatches - 1
        while matchesIx >= 0 and len(ret) < numToFetch:
            for match in matches[matchesIx]:
                _addUser(ret, match, aviOnly)
                if len(ret) >= numToFetch:
                    break
            matchesIx -= 1
        return {'data': ret}

# send a request to SoundCloud
# NOTE as of May 10th, 2016, the max limit is 200, any higher limit results in an error
def sendQuery(request, type, limit):
    if limit > 200:
        limit = 200
    # spawn a generic client
    client = getGenericClient()
    ret = None
    if (type == RequestType.friends):
        query = request.json['query']
        numToFetch = int(request.json['numToFetch'])
        aviOnly = request.json['aviOnly']
        city = request.json['city']
        country = request.json['country']
        if numToFetch < 200 and aviOnly == False and city == "" and country == "":
            # set the limit to the number to fetch since they're not filtering
            limit = numToFetch
        ret = client.get(
            '/users',
            q = query,
            limit = limit
        )
        if len(ret) >= numToFetch:
            ret = getUsers(ret, numToFetch, aviOnly, city, country)
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
    return toJson(ret)
