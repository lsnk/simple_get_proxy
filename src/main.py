import argparse

import uvicorn


def comma_separated(string):
    return [s.lower() for s in string.split(',')]


parser = argparse.ArgumentParser(description='Simple GET proxy.')

parser.add_argument(
    'url', metavar='URL', type=str,
    help='an URL to proxy requests')

parser.add_argument(
    '--skip',
    metavar='SKIP', type=comma_separated, default=[],
    help='Comma-separated list of GET params to exclude from requests.'
)
parser.add_argument(
    '--cache',
    metavar='CACHE', type=int, default=None,
    help='Cache duration in seconds.'
)


if __name__ == "__main__":
    uvicorn.run(
        "server:app_factory",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True,
    )
