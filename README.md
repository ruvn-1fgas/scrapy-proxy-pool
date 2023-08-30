scrapy-proxy-pool
=======================

[![Scrapy](https://camo.githubusercontent.com/40d00cefb120a829517e503658aaf6c987d5f9cc6be5e2e35fb20bd63bdbceb5/68747470733a2f2f7363726170792e6f72672f696d672f7363726170796c6f676f2e706e67)](https://scrapy.org/)

Initially made by [rejoiceinhope](https://github.com/rejoiceinhope), modified by me.

Changes
-------
* Added support for Python 3.11
* Added setting `PROXY_POOL_URLS` - list of proxies in either format `http://<ip>:<port>` or `http://<user>:<pass>@<ip>:<port>`



Installation
------------
```pip install .```

Usage
-----

Enable this middleware by adding the following settings to your settings.py::

    PROXY_POOL_ENABLED = True

Then add rotating_proxies middlewares to your DOWNLOADER_MIDDLEWARES::

    DOWNLOADER_MIDDLEWARES = {
        # ...
        'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
        'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
        # ...
    }

After this all requests will be proxied using proxies.

Requests with "proxy" set in their meta are not handled by
scrapy-proxy-pool. To disable proxying for a request set
``request.meta['proxy'] = None``; to set proxy explicitly use
``request.meta['proxy'] = "<my-proxy-address>"``.


Concurrency
-----------

By default, all default Scrapy concurrency options (``DOWNLOAD_DELAY``,
``AUTHTHROTTLE_...``, ``CONCURRENT_REQUESTS_PER_DOMAIN``, etc) become
per-proxy for proxied requests when RotatingProxyMiddleware is enabled.
For example, if you set ``CONCURRENT_REQUESTS_PER_DOMAIN=2`` then
spider will be making at most 2 concurrent connections to each proxy,
regardless of request url domain.

Customization
-------------

``scrapy-proxy-pool`` keeps track of working and non-working proxies from time to time.

Detection of a non-working proxy is site-specific.
By default, ``scrapy-proxy-pool`` uses a simple heuristic:
if a response status code is not 200, 301, 302, 404, 500, response body is empty or if
there was an exception then proxy is considered dead.

You can override ban detection method by passing a path to
a custom BanDectionPolicy in ``PROXY_POOL_BAN_POLICY`` option, e.g.::

    # settings.py
    PROXY_POOL_BAN_POLICY = 'myproject.policy.MyBanPolicy'

The policy must be a class with ``response_is_ban``
and ``exception_is_ban`` methods. These methods can return True
(ban detected), False (not a ban) or None (unknown). It can be convenient
to subclass and modify default BanDetectionPolicy::

    # myproject/policy.py
    from scrapy_proxy_pool.policy import BanDetectionPolicy

    class MyPolicy(BanDetectionPolicy):
        def response_is_ban(self, request, response):
            # use default rules, but also consider HTTP 200 responses
            # a ban if there is 'captcha' word in response body.
            ban = super(MyPolicy, self).response_is_ban(request, response)
            ban = ban or b'captcha' in response.body
            return ban

        def exception_is_ban(self, request, exception):
            # override method completely: don't take exceptions in account
            return None

Instead of creating a policy you can also implement ``response_is_ban``
and ``exception_is_ban`` methods as spider methods, for example::

    class MySpider(scrapy.Spider):
        # ...

        def response_is_ban(self, request, response):
            return b'banned' in response.body

        def exception_is_ban(self, request, exception):
            return None

It is important to have these rules correct because action for a failed
request and a bad proxy should be different: if it is a proxy to blame
it makes sense to retry the request with a different proxy.

Settings
--------

* ``PROXY_POOL_ENABLED``  - Whether enable ProxyPoolMiddleware;
* ``PROXY_POOL_REFRESH_INTERVAL`` - proxies refresh interval in seconds, 900 by default;
* ``PROXY_POOL_LOGSTATS_INTERVAL`` - stats logging interval in seconds,
  30 by default;
* ``PROXY_POOL_CLOSE_SPIDER`` - When True, spider is stopped if
  there are no alive proxies. If False (default), then when there is no
  alive proxies all dead proxies are re-checked.
* ``PROXY_POOL_URLS`` - a list of urls to crawl proxies from.
* ``PROXY_POOL_PAGE_RETRY_TIMES`` - a number of times to retry
  downloading a page using a different proxy. After this amount of retries
  failure is considered a page failure, not a proxy failure.
  Think of it this way: every improperly detected ban cost you
  ``PROXY_POOL_PAGE_RETRY_TIMES`` alive proxies. Default: 5.

  It is possible to change this option per-request using
  ``max_proxies_to_try`` request.meta key - for example, you can use a higher
  value for certain pages if you're sure they should work.
* ``PROXY_POOL_TRY_WITH_HOST`` - When True, spider will try requests that exceed PROXY_POOL_PAGE_RETRY_TIMES.
* ``PROXY_POOL_BAN_POLICY`` - path to a ban detection policy.
  Default is ``'scrapy_proxy_pool.policy.BanDetectionPolicy'``.
