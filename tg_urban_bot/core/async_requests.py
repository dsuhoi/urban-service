import json

import aiohttp
from config import CONFIG


class aio_requests:
    def __init__(self, base_url=None, session=None, optimize=False, **session_params):
        if optimize:
            session_params["skip_auto_headers"] = {"User-Agent"}
            session_params["raise_for_status"] = False
        self.base_url = base_url
        self.__session = session
        self.__session_params = session_params

    def __del__(self):
        if self.__session and not self.__session.closed:
            if (
                self.__session._connector is not None
                and self.__session._connector_owner
            ):
                self.__session._connector.close()
            self.__session._connector = None

    async def close(self):
        if self.__session and not self.__session.closed:
            await self.session.close()

    async def _request(self, url: str, method: str = "GET", data=None, **kwargs):
        if not self.__session:
            self.__session = aiohttp.ClientSession(
                base_url=self.base_url,
                json_serialize=json.dumps,
                **self.__session_params
            )
        async with self.__session.request(
            url=url, method=method, data=data, **kwargs
        ) as response:
            await response.read()
            return response

    async def request_text(self, url: str, method: str = "GET", data=None, **kwargs):
        response = await self._request(url, method, data, **kwargs)
        return await response.text(encoding="utf-8")

    async def request_json(self, url: str, method: str = "GET", data=None, **kwargs):
        response = await self._request(url, method, data, **kwargs)
        return await response.json(
            encoding="utf-8", loads=json.loads, content_type=None
        )

    async def request_content(self, url: str, method: str = "GET", data=None, **kwargs):
        response = await self._request(url, method, data, **kwargs)
        return response._body


aioreq = aio_requests(base_url=CONFIG.SERVER_URL)
