# -*- coding: utf-8 -*-

import asyncio


class EnsureCorotineMethod(type):
    ''' metaclass to ensure specified methods to be coroutinefunction
    '''
    def __init__(cls, name, bases, kwargs):
        names = getattr(cls, '__coroutines__', [])
        for name in names:
            method = kwargs.get(name, None)
            if not callable(method):
                continue
            if not asyncio.iscoroutinefunction(method):
                method = asyncio.coroutine(method)
                setattr(cls, name, method)
        super().__init__(name, bases, kwargs)


def ensure_coroutine(func):
    ''' ensure the func is a coroutinefunction
    '''
    assert callable(func)
    if not asyncio.iscoroutinefunction(func):
        func = asyncio.coroutine(func)
    return func
