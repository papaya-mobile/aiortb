# -*- coding: utf-8 -*-

__all__ = ['RTBServer']

import copy

import asyncio
from aiohttp.web import Application, Response
from aiohttp import hdrs

from .publisher import AbstractPublisher
from .aution import AbstractAutionPolicy
from .log import logger


class RTBServer(object):
    def __init__(self, name='', openrtb_version=''):
        self.name = name or 'aiortb'
        self.openrtb_version = openrtb_version

        self._publishers = {}
        self._bidders = []
        self._auction_policy = None

        self._is_running = False

    def _get_auction_policy(self):
        return self._auction_policy

    def _set_auction_policy(self, policy):
        assert isinstance(policy, AbstractAutionPolicy)
        self._auction_policy = policy

    auction_policy = property(_get_auction_policy, _set_auction_policy)

    def add_publisher(self, name, path, method, publisher_factory):
        assert not self._is_running
        self._publishers[(name, path, method)] = publisher_factory

    def add_bidder(self, bidder_factory):
        assert not self._is_running
        self._bidders.append(bidder_factory)

    def _add_routes(self, app):
        for key, publisher_factory in self._publishers.items():
            name, path, method = key

            async def handle(request):
                publisher = publisher_factory()
                return (await self._handle(publisher, request))

            app.router.add_route(method, path=path, handler=handle, name=name)

    async def _handle(self, publisher, request):
        assert isinstance(publisher, AbstractPublisher)

        try:
            request = await publisher.parse_request(request)
            bid_responses = await self._broadcast(request)
            winner, resp = (await self.auction_policy.auction(bid_responses))
            resp = await publisher.prepare_response(winner, resp)
        except Exception as e:
            try:
                resp = await publisher.fallback(e)
            except Exception as e:
                logger.exception("Error During Fallback")
                resp = Response(status=500)
            else:
                logger.exception("Error which has been lucky fallback")

        resp.headers[hdrs.SERVER] = self.name
        if self.openrtb_version:
            resp.headers[hdrs.upstr('x-openrtb-version')] = \
                self.openrtb_version
        return resp

    async def _broadcast(self, request):
        resps = {}

        if not self._bidders:
            return resps

        bids = {}
        for bidder_factory in self._bidders:
            bidder = bidder_factory()
            bid = asyncio.coroutine(bidder.bid)
            fu = asyncio.ensure_future(bid(copy.deepcopy(request)))
            bids[fu] = bidder

        if not bids:
            return resps

        done, _ = await asyncio.wait(bids.keys(), timeout=0.1)

        for fu in done:
            bidder = bids[fu]
            try:
                resps[bidder] = fu.result()
            except asyncio.CancelledError:
                pass
            except Exception:
                logger.exception('Bidder Exception')

        # We in fact need to do nothing to the pending futures since
        # python3 gc will collect them

        return resps

    def run(self, host='127.0.0.1', port=8090):
        self._is_running = True

        loop = asyncio.get_event_loop()
        self._app = app = Application()

        self._add_routes(app)

        handler = app.make_handler()
        srv = loop.create_server(handler, host=host, port=port)
        srv = loop.run_until_complete(srv)

        logger.info('serving on {}'.format(srv.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.run_until_complete(handler.finish_connections(1.0))
            srv.close()
            loop.run_until_complete(srv.wait_closed())
            loop.run_until_complete(app.finish())

        loop.close()
