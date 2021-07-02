from urllib.parse import urljoin

import aiohttp
from cachetools import TTLCache


class Client:

    def __init__(self, base_url, cache_ttl=None):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()
        if cache_ttl is not None:
            self.cache = TTLCache(256, ttl=cache_ttl)

    def _build_full_url(self, path):
        return urljoin(self.base_url, path)

    async def get(self, path, query_params):
        return await self.session.get(
            self._build_full_url(path), params=query_params
        )
