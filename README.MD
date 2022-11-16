# SIMPLE GET PROXY

## A tool to proxy HTTP GET requests to specified server.

### Local deployment

```
python -m venv .venv
pip install pipenv
pipenv install --deploy

cd src
python main.py <url>
```

### Docker deployment

...

### Additional parameters

- `--skip <param1,param2>` is used to exclude some query parameters from request (I use it to disable caching in Google Sheets)
- `--cache <sec>` caches responses for specified amount of seconds.

### My use cases

I use this tool primarily to access external APIs inside Google Sheets like this:

`... https://<api_url> --skip seed --cache 300`

And in a Google Sheets formula something like:

`ImportJSON(CONCATENATE(<endpoint>;"?seed=";<seed cell>;&;<rest query params>"))`

Example APIs:
- `https://api.binance.com`
- `https://api.coingecko.com`
