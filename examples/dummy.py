# -*- coding: utf-8 -*-

import random
import asyncio
from aiohttp.web import Response
import logging

from aiortb import RTBServer
from aiortb import AbstractPublisher, AbstractBidder
from aiortb import AbstractAutionPolicy


class DummyPublisher(AbstractPublisher):
    def parse_request(self, request):
        if random.random() < 0.1:
            raise Exception("DummyPublisher.parse_request")
        return {'bid': 'dummy'}

    def prepare_response(self, win_bidder, response):
        if random.random() < 0.1:
            raise Exception("DummyPublisher.prepare_response")
        if response:
            return Response(status=200, text=str(response))
        else:
            return Response(status=204)

    def fallback(self, exe):
        if random.random() < 0.5:
            raise Exception("DummyPublisher.prepare_response")
        return Response(status=200, text='fallback')


class DummyBidder(AbstractBidder):
    async def bid(self, request):
        if random.random() < 0.1:
            raise Exception("DummyBidder.001")
        request['price'] = random.random()
        await asyncio.sleep(0.2 * random.random())
        if random.random() < 0.1:
            raise Exception("DummyBidder.002")
        return request


class RandomAutionPolicy(AbstractAutionPolicy):
    def auction(self, bid_responses):
        if not bid_responses:
            return (None, None)

        bidder = random.choice(list(bid_responses.keys()))
        return (bidder, bid_responses[bidder])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    server = RTBServer()
    server.add_publisher('dummy', '/', 'POST', DummyPublisher)
    server.add_bidder(DummyBidder)
    server.add_bidder(DummyBidder)
    server.add_bidder(DummyBidder)
    server.auction_policy = RandomAutionPolicy()

    server.run()
