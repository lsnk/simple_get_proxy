from urllib.parse import urljoin

import aiohttp


class Client:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

    def _build_full_url(self, path):
        return urljoin(self.base_url, path)

    async def get(self, path, query_params):
        return await self.session.get(
            self._build_full_url(path), params=query_params
        )
