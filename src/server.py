from aiohttp import ClientResponse
from starlette.applications import Starlette
from starlette.responses import Response as ServerResponse
from starlette.routing import Route

from client import Client


async def serve(request):
    client_response: ClientResponse = await request.app.remote_service_client.get(
        request.path_params['rest_of_path'], dict(request.query_params)
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

    return app
