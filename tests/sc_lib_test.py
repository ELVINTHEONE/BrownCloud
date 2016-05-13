import os
import pytest

os.environ['BASE_URI'] = ''
os.environ['CLIENT_ID'] = ''
os.environ['CLIENT_SECRET'] = ''
os.environ['AUTH_REDIRECT'] = ''
os.environ['DEFAULT_AVI_URL'] = 'http://a1.sndcdn.com/images/default_avatar_large.png'

DEFAULT_AVI_URL = os.environ['DEFAULT_AVI_URL']

from lib.sc_lib import getUsers

class User:
    def __init__(self, avi_url, city, country):
        self.avatar_url = avi_url
        self.city = city
        self.country = country

#                 u1      u2      u3      u4      u5      u6
#     avi         x.com   x.com   y.com   y.com   z.com   z.com
#     city        a       b       a       c       b       c
#     country     d       e       e       f       d       f
def test_returnsUsersWithMostMatchingCriteria():
    u1 = User('x.com', 'a', 'd')
    u2 = User('x.com', 'b', 'e')
    u3 = User('y.com', 'a', 'e')
    u4 = User('y.com', 'c', 'f')
    u5 = User('z.com', 'b', 'd')
    u6 = User('z.com', 'c', 'f')
    users = [u1, u2, u3, u4, u5, u6]

    print("get 2 users from city 'a'")
    ret = getUsers(users, 2, False, 'a', 'NA')['data']
    assert u1 in ret and u3 in ret

    print("get 3 users from city 'a' and country 'e'")
    ret = getUsers(users, 3, False, 'a', 'e')['data']
    assert u1 in ret[0:2] and u3 in ret[0:2] and u2 == ret[2], "u1 and u3 are the first two returned, u2 is the last item in the list"

def test_doesNotAddUsersWithoutAnAvi():
    u1 = User(DEFAULT_AVI_URL, 'a', 'b')
    u2 = User('x.com', 'a', 'b')
    ret = getUsers([u1, u2], 2, True, 'a', 'b')['data']
    assert len(ret) == 1 and ret[0] == u2