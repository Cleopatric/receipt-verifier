""" Module with client instance. """
import aiohttp
import asyncio

from aiohttp import ClientSession


class HttpClient:
    """ Async HTTP Client. """

    @staticmethod
    async def fetch(session, url: str, params: dict = None) -> dict:
        """ Make async POST requests.

        :param session: client session.
        :param url:     url for request.
        :param params:  params data for getting request.
        :return:        dict with request data.
        """
        async with session.post(url, data=params) as response:
            return await response.json(content_type=None)

    async def get_response(self, referer: str, params: list) -> list:
        """ Create tasks with requests.

        :param referer: base url.
        :param params:  params data for getting request.
        :return:        result of requests.
        """
        tasks = []
        timeout = aiohttp.ClientTimeout(total=60)
        async with ClientSession(headers={"Referer": referer}, timeout=timeout) as session:
            for param in params:
                task = asyncio.ensure_future(self.fetch(session, referer, param))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            return responses

    async def get_api_data(self, referer: str, params: list) -> list:
        """ Get API responses using base url.

        :param referer: base url.
        :param params:  params for get request.
        :return:        result of requests.
        """
        return await asyncio.ensure_future(self.get_response(referer, params))
