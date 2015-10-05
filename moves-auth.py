from moves import api
from moves import auth
from moves.util import *

import argparse
import webbrowser
import os

__author__ = 'iwharris'


if __name__ == '__main__':
    # Get arguments
    parser = argparse.ArgumentParser(description='Handles authorization for Moves API.')
    parser.add_argument('-client_id', nargs='?', default='', help='The Client ID to use.')
    parser.add_argument('-client_secret', nargs='?', default='', help='The Client Secret to use.')
    parser.add_argument('-scope', nargs='?', default='activity location', help='"activity" or "location", or both (space-delimited)')
    parser.add_argument('-redirect_uri', nargs='?', default='localhost', help='The URI to redirect to after authentication operations.')
    parser.add_argument('-state', nargs='?', default='Optional parameter that is passed and returned from auth calls.')
    # parser.add_argument('-auth_code', nargs='?', default='', help='Gets an access code from the server.')
    parser.add_argument('--browser_auth', action='store_true', help='Runs an authorization request in the browser.')
    parser.add_argument('--auth', action='store_true', help='Runs an authorization request in the console.')
    # parser.add_argument('--access_token', action='store_true', help='Gets an access token using client credentials.')
    args = parser.parse_args()

    # Client ID is mandatory
    client_id = args.client_id
    if not client_id:  # Attempt to get client id from env
        client_id = os.getenv('MT_CLIENT_ID', None)
    client_secret = args.client_secret
    if not client_secret:
        client_secret = os.getenv('MT_CLIENT_SECRET', None)
    scope = args.scope
    redirect_uri = args.redirect_uri
    state = args.state

    if args.browser_auth:
        assert client_id, "client_id must be set in arguments or in the MT_CLIENT_ID env variable."
        params = {
            'response_type': 'code',
            'client_id': client_id,
            'scope': scope,
            'redirect_uri': redirect_uri,
            'state': state,
        }
        url = build_url(api.BASE_AUTH_URL + '/authorize', params)
        webbrowser.open(url)

    elif args.auth:
        assert client_id, "client_id must be set in arguments or in the MT_CLIENT_ID env variable."
        assert client_secret, "client_secret must be set in arguments or in the MT_CLIENT_SECRET env variable."
        url = api.BASE_API_URL
        auth_object = auth.request_auth_desktop(api.BASE_AUTH_URL, client_id, client_secret, scope, redirect_uri, state)
        if auth_object:
            print('Received authorization code: %s' % auth_object)
        else:
            print('Failed to obtain authorization code.')

    # elif args.access_token:
    #     assert client_id, "client_id must be set in arguments or in the MT_CLIENT_ID env variable."
    #     assert client_secret, "client_secret must be set in arguments or in the MT_CLIENT_SECRET env variable."
    #     assert auth_code, "auth_code must be set in arguments or in the MY_AUTH_CODE env variable."
    #     access_token_object = auth.request_access_token(api.BASE_AUTH_URL + '/access_token', auth_code, client_id, client_secret, redirect_uri)
    #     if access_token_object:
    #         print('Got access token: %s' % access_token_object)
    #     else:
    #         print('Did not get access token.')
    else:
        parser.print_help()
