from typing import Dict


def get_token_from_headers(headers: Dict[str, str]) -> str:
    if "HTTP_AUTHORIZATION" in headers:
        authorization = headers.get("HTTP_AUTHORIZATION")
        token = authorization.split(":")[1].strip()
        return token[7:]
    return ""
