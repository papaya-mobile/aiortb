# -*- coding: utf-8 -*-

__all__ = ['AbstractBidder']

from .utils import EnsureCorotineMethod


class AbstractBidder(metaclass=EnsureCorotineMethod):
    __coroutines__ = ['bid']

    async def bid(self, request):
        ''' perform a bid due to the request.
        request:
            an object, the request from publisher

        We should do the following things:

            1. prepare request due to requirements of the bidder
            2. perform a request by using http client got from
               httpclient.get_httpclient()
            3. parse the response and return it

        which can be descripted in pseudocode:

            request = self.prepare_request(request)
            resp = await get_http_client().post(self.url, request)
            resp = self.parse_response(resp)
            return resp
        '''
        raise NotImplementedError
