# -*- coding: utf-8 -*-

'''
Http client used to perform request onto bidders.
The client is a global and is an instance of aiohttp.ClientSession.
The default client will be installed by the first call of
get_http_client(). Also you can customize by calling set_http_client().
'''

__all__ = ['get_http_client', 'set_http_client']

import aiohttp


# The global http client.
_http_client = None


def get_http_client():
    global _http_client
    if _http_client is None:
        _http_client = aiohttp.ClientSession()
    return _http_client


def set_http_client(client):
    global _http_client
    assert client is None or isinstance(client, aiohttp.ClientSession)
    _http_client = client
