from __future__ import print_function
import requests
import time
import sys
from lxml import html
import urlparse

from util import *

__author__ = 'iwharris'


def request_auth_desktop(base_url, client_id, client_secret, scope, redirect_uri, state=''):
    """Makes an auth request to the Moves API.
    scope may be 'activity', 'location', or both (space-delimited)
    redirect_uri must match a Redirect URI set in your app's Development config (https://dev.moves-app/com)
    """
    parameters = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state,
    }
    # Initiate a session
    session = requests.session()
    auth_page = session.get(base_url + '/authorize', params=parameters)
    print(auth_page.url)
    if auth_page.status_code != requests.codes.ok:
        auth_page.raise_for_status()
    # print(auth_page.text)
    # Scrape auth page for some useful info
    tree = html.fromstring(auth_page.text)

    # Get auth token (contained in a form element)
    auth_token_elements = tree.xpath('//input[@name="auth_token"]')
    auth_token = auth_token_elements[0].value

    # Get pin code (contained in two span elements)
    pin_pair = tree.xpath('//span[@class="digitgroup"]/text()')
    pin_code = ''.join(pin_pair)
    # Request code is just the pin with last digit omitted
    request_code = pin_code[:-1]

    # Display waiting message to user
    print('Please enter this pin code into the Moves app: %s' % (' '.join(pin_pair)))

    # Loop while making checkAuthorized requests
    auth_result = request_check_authorized(base_url + '/checkAuthorized', client_id, session, request_code, auth_token)
    if auth_result != 'authorize':
        return False
    authorization_code = request_authorize_redirect(base_url + '/authorizeAndRedirect', client_id, session, request_code, auth_token, scope, redirect_uri, state)

    # return authorization_code
    authorization_obj = request_access_token(session, base_url + '/access_token', authorization_code, client_id, client_secret, redirect_uri)
    return authorization_obj


def request_check_authorized(url, client_id, session, request_code, auth_token, timeout=90, interval=2):
    assert client_id, "client_id must be set in arguments or in the MT_CLIENT_ID env variable."
    payload = {
        'request_code': request_code,
        'client_id': client_id,
        'auth_token': auth_token,
    }
    timeout_time = time.time() + timeout
    is_finished = False
    finished_result = ''
    print('Waiting for user to authorize the app.', end="")
    while (not is_finished) and (time.time() < timeout_time):
        response = session.post(url, data=payload)
        if response.status_code == requests.codes.ok:
            status = response.json()['status']
            if status == 'pending':
                print('.', end="")
            elif status == 'authorize':
                print('authorized!')
                is_finished = True
                finished_result = status
            elif status == 'cancel':
                print('cancelled.')
                is_finished = True
                finished_result = status
        else:
            is_finished = True
            finished_result = 'error'
            print('encountered an error.')
            print("%s %s" % (response.status_code, response.text), file=sys.stderr)
        if not is_finished:
            time.sleep(interval)
    # End while
    if time.time() > timeout_time:
        print('timed out after %d seconds.' % timeout)
    return finished_result


def request_authorize_redirect(url, client_id, session, request_code, auth_token, scope, redirect_uri, state=''):
    """Using the auth session, obtains an auth code.
    The auth code can then be exchanged for an access token.
    """
    assert client_id, "client_id must be set in arguments or in the MT_CLIENT_ID env variable."
    payload = {
        'auth_token': auth_token,
        'request_code': request_code,
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope,
        'state': state,
        'error_uri': redirect_uri,
    }
    response = session.post(url, data=payload)
    # We don't care about response code - we just want the 'code' URL parameter
    p = urlparse.urlparse(response.url)
    return urlparse.parse_qs(p.query)['code'][0]


def request_access_token(session, url, auth_code, client_id, client_secret, redirect_uri):
    parameters = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
    }
    url = build_url(url, parameters)
    response = session.post(url)
    print(response.url)
    if (response.status_code == requests.codes.ok):
        auth_object = response.json()
        return auth_object
    else:
        response.raise_for_status()