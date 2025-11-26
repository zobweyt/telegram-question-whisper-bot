import urllib.parse


def strip_url_scheme(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    scheme = "%s://" % parsed.scheme
    return parsed.geturl().replace(scheme, "", 1)
