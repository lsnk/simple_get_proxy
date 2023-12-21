import asyncio
import json

from aiohttp import ClientResponse
from cachetools import TTLCache
from starlette.applications import Starlette
from starlette.responses import Response as ServerResponse
from starlette.routing import Route

from client import Client


def _clean_query_params(query_params, skip_list):
    query_params = {
        k.lower(): v for k, v in query_params.items()
    }

    for param_name in skip_list:
        query_params.pop(param_name, None)

    return query_params


def _get_cache_key(path, query_params):
    return json.dumps((path, query_params))


async def serve(request):
    path = request.path_params['rest_of_path']
    query_params = _clean_query_params(
        request.query_params, request.app.skip_list
    )

    cache = request.app.cache
    if cache is not None:
        key = _get_cache_key(path, query_params)
        response_data = cache.get(key)
        if response_data is not None:
            return ServerResponse(**response_data)

    client_response: ClientResponse = await request.app.remote_service_client.get(
        path,
        query_params,
    )

    for _ in range(3):

        async with client_response:
            if client_response.status in (429, 500):
                await asyncio.sleep(5)
                continue

            response_headers = dict(client_response.headers)

            # ignoring some headers
            response_headers.pop('Content-Encoding', None)
            response_headers.pop('Content-Length', None)

            response_data = dict(
                content=await client_response.read(),
                status_code=client_response.status,
                headers=response_headers,
            )
            if cache is not None:
                key = _get_cache_key(path, query_params)
                cache[key] = response_data

            return ServerResponse(**response_data)

routes = [
    Route("/{rest_of_path:path}", endpoint=serve, methods=['GET']),
]


def app_factory(*args, **kwargs):
    from main import parser
    args = parser.parse_args()

    app = Starlette(routes=routes)
    app.remote_service_client = Client(args.url)
    app.skip_list = args.skip
    app.cache = TTLCache(256, ttl=args.cache) if args.cache is not None else None

    return app
