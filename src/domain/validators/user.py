import re


def validate_user_url(url: str) -> str:
    if re.search(r"[^a-zA-Z0-9-_]", url):
        raise ValueError("User URL must contain only A-Z, a-z, 0-9, _ and -")

    if len(url) > 64:
        raise ValueError("User URL must be up to 64 characters long.")

    return url
