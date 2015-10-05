from __future__ import print_function

from auth import *
import requests
import time
import sys
from lxml import html
import urlparse

__author__ = 'iwharris'

BASE_API_URL = 'https://api.moves-app.com/api/1.1'
BASE_AUTH_URL = 'https://api.moves-app.com/oauth/v1'
BASE_AUTH_CHECK_URL = BASE_AUTH_URL + '/checkAuthorized'
BASE_AUTH_CHECK_REDIRECT_URL = BASE_AUTH_URL + '/authorizeAndRedirect'


class MovesAPI(object):

    def __init__(self, client_id='', client_secret='', authorization_code=''):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_code = authorization_code








