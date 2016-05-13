import os
import json
from enum import Enum
import soundcloud

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
AUTH_REDIRECT = os.environ['AUTH_REDIRECT']
DEFAULT_AVI_URL = os.environ['DEFAULT_AVI_URL']

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
    return DEFAULT_AVI_URL not in user.avatar_url

# add the user, check if 'avatar-only' is true, if so, then make sure the user has an avatar
def _addUser(ret, user, aviOnly):
    if not aviOnly or _hasAvi(user):
        ret.append(user)

# filter out the users who have an avatar
def _filterUsersWithAvi(users):
    return list(filter(lambda user: _hasAvi(user), users))

# process the users returned from SoundCloud
def getUsers(users, numToFetch, aviOnly, city, country):
    ret = []
    if len(users) <= numToFetch:
        # return the users
        if aviOnly:
            ret = _filterUsersWithAvi(users)
        else:
            ret = users
    elif numToFetch > 0:
        # match the users to each of the criteria, rate them based on number matched
        matches = dict({
            0: [], 1: []
        })
        maxMatches = 2
        for user in users:
            matchCount = 0
            if aviOnly and DEFAULT_AVI_URL in user.avatar_url:
                continue # skip users with no avatar when we want avi-only users
            if user.city == city:
                matchCount += 1
            if user.country == country:
                matchCount += 1
            if matchCount == maxMatches:
                # add the user to the array directly
                _addUser(ret, user, aviOnly)
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
            q = "{0} {1} {2}".format(query, city, country),
            limit = limit
            )
        if len(ret) == 0:
            # try again with just the user name
            ret = client.get(
                '/users',
                q = query,
                limit = limit
                )
        if len(ret) >= numToFetch:
            ret = getUsers(ret, numToFetch, aviOnly, city, country)
        elif aviOnly:
            ret = {'data': _filterUsersWithAvi(ret)}
    elif (type == RequestType.tracks):
        query = request.json['query']
        ret = client.get(
            '/tracks',
            q = query,
            tags = request.json['tags'],
            filter = request.json['visibility'],
            license = request.json['license'],
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
