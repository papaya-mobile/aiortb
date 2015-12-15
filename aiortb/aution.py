# -*- coding: utf-8 -*-

__all__ = ['AbstractAutionPolicy']

from .utils import EnsureCorotineMethod


class AbstractAutionPolicy(metaclass=EnsureCorotineMethod):
    __coroutines__ = ['auction']

    async def auction(self, bid_responses):
        ''' auction and return the winner
        bid_responses:  dict, {bidder: bid_resp}
        return: win_response
        '''
        raise NotImplementedError
