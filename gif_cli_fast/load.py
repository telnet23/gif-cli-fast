import base64
import os
import requests


def _giphy(query, cache):
    url = requests.get(
        "https://api.giphy.com/v1/gifs/" + ("search" if query else "trending"),
        params={
            "api_key": os.getenv("GIPHY_API_KEY", "VtFOP3GgfrPo3KPWfjw0U5g8aD6VtIHi"),
            "q": query,
            "limit": 1,
            "lang": "en",
        },
    ).json()["data"][0]["images"]["downsized"]["url"]
    return _get(url, cache)


def _tenor(query, cache):
    url = requests.get(
        "https://g.tenor.com/v1/" + ("search" if query else "trending"),
        params={
            "key": os.getenv("TENOR_API_KEY", "TQ7VXFHXBJQ5"),
            "q": query,
            "locale": "en_US",
            "limit": 1,
        },
    ).json()["results"][0]["media"][0]["tinygif"]["url"]
    return _get(url, cache)


def _local(query, _cache):
    return open(query, "rb").read()


_LOADERS = {
    "giphy": _giphy,
    "tenor": _tenor,
    "local": _local,
}


def load(provider, query, cache):
    loader = _LOADERS[provider]

    try:
        return loader(query, cache)
    except (IndexError, KeyError, FileNotFoundError):
        return None


def _get(url, cache):
    os.makedirs(cache, exist_ok=True)
    os.chdir(cache)

    key = base64.b64encode(url.encode("ascii")).decode("ascii").replace("/", "_")

    if os.path.exists(key):
        return open(key, "rb").read()

    content = requests.get(url).content
    open(key, "wb").write(content)
    return content
