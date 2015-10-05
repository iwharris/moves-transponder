import urllib

__author__ = 'iwharris'


def build_url(url, parameters={}):
    return "%s?%s" % (url, urllib.urlencode(parameters))
