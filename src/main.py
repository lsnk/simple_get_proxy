import argparse

import uvicorn

parser = argparse.ArgumentParser(description='Simple GET proxy.')
parser.add_argument('url', metavar='URL', type=str,
                    help='an URL to proxy requests')


if __name__ == "__main__":
    uvicorn.run(
        "server:app_factory",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True,
    )
