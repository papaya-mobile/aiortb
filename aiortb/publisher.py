# -*- coding: utf-8 -*-

__all__ = ['AbstractPublisher']

from .utils import EnsureCorotineMethod


class AbstractPublisher(metaclass=EnsureCorotineMethod):
    __coroutines__ = ['parse_request', 'prepare_response', 'fallback',]

    async def parse_request(self, request):
        ''' parse raw request
        return: dict of bid request
        '''
        raise NotImplementedError

    async def prepare_response(self, win_bidder, response):
        ''' prepare response
        response: dict of bid response
        return: aiohttp.Response
        '''
        raise NotImplementedError

    async def fallback(self, exe):
        ''' fallback when exception raised
        exe: an Exception instance
        return: aiohttp.Response
        '''
        raise NotImplementedError
