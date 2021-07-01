from aiohttp import ClientResponse
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


async def serve(request):
    client_response: ClientResponse = await request.app.remote_service_client.get(
        request.path_params['rest_of_path'],
        _clean_query_params(request.query_params, request.app.skip_list),
    )

    async with client_response:
        return ServerResponse(
            content=await client_response.read(),
            status_code=client_response.status,
            headers=dict(client_response.headers),
        )

routes = [
    Route("/{rest_of_path:path}", endpoint=serve, methods=['GET']),
]


def app_factory(*args, **kwargs):
    from main import parser
    args = parser.parse_args()

    app = Starlette(routes=routes)
    app.remote_service_client = Client(args.url)
    app.skip_list = args.skip

    return app
