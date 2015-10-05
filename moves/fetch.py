__author__ = 'KainokiKaede'

"""
1. Go to https://dev.moves-app.com/apps and register a new app.
   client_id and client_secret will be given, so paste it to the variables below.
2. `$ python fetch.py --requesturl` will open the web browser.
   Follow the instructions and authenticate the app.
   You will be redirected to a web page with an error message.
   Copy the string between `code=` and `&`.
   That is your request_token, so paste it below.
3. `$ python fetch.py --accesstoken` will output access token to stdout.
   Copy the token and paste it below.
4. `$ python fetch.py YYYYMMDD YYYYMMDD` will create the json file between
   the days you specified.
5. If you need the file in gpx, please consider using my `json2gpx.py`.
"""
import requests
import datetime
import time
import json
import argparse
import webbrowser

client_id = ''
client_secret = ''
request_token = ''
access_token = ''

api_url = 'https://api.moves-app.com/api/1.1'
oauth_url = 'https://api.moves-app.com/oauth/v1'

def create_request_url():
    url = oauth_url
    url += '/authorize?response_type=code'
    url += '&client_id=' + client_id
    url += '&scope=activity%20location'
    return url

def get_access_token():
    url = oauth_url
    url += '/access_token?grant_type=authorization_code'
    url += '&code=' + request_token
    url += '&client_id=' + client_id
    url += '&client_secret=' + client_secret
    url += '&redirect_uri='
    responce = requests.post(url)
    access_token = responce.json()['access_token']
    return access_token

def get(access_token, endpoint):
    url = api_url
    url += endpoint
    url += '?access_token=' + access_token
    return requests.get(url).json()

def get_storyline(access_token, date):
    url = api_url
    url += '/user/storyline/daily/{date}'.format(date=date.strftime('%Y%m%d'))
    url += '?trackPoints=true'
    url += '&access_token=' + access_token
    return requests.get(url).json()

def get_storylines(access_token, startdate, enddate, wait_sec=3):
    a_day = datetime.timedelta(days=1)
    date = startdate
    storylines = []
    while date <= enddate:
        print date.strftime('%F')
        try:
            storyline = get_storyline(access_token, date)
        except:
            storyline = []
            print 'Error occured on {date}'.format(date=date.strftime('%F'))
        storylines.append(storyline)
        if date == enddate: wait_sec = 0
        time.sleep(wait_sec)
        date += a_day
    return storylines


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Fetch Storyline in JSON file from Moves API.')
    parser.add_argument('startdate', nargs='?', default=None)
    parser.add_argument('enddate', nargs='?', default=None)
    parser.add_argument('--requesturl', action='store_true')
    parser.add_argument('--accesstoken', action='store_true')
    parser.add_argument('--stdout', action='store_true')
    args = parser.parse_args()

    if args.requesturl:
        url = create_request_url()
        print url
        webbrowser.open(url)

    elif args.accesstoken:
        print get_access_token()

    else:
        assert args.startdate is not None
        startdate = datetime.datetime.strptime(args.startdate, '%Y%m%d')
        if args.enddate is None:
            enddate = startdate
        else:
            enddate = datetime.datetime.strptime(args.enddate, '%Y%m%d')
        storylines = get_storylines(access_token, startdate, enddate)
        storylines_json = json.dumps(storylines, indent=4)
        if not args.stdout:
            outfilename = startdate.strftime('%F') + '-' + enddate.strftime('%F')
            outfilename += '-moves-storyline.json'
            outfile = open(outfilename, 'w')
            outfile.write(storylines_json)
            outfile.close()
        else: print storylines_json