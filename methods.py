import requests


def get_request_proxy(path: str, key: str, headers=None, params=None):

    response = requests.get(path, headers=headers, params=params)
    response.raise_for_status()

    try:
        data = response.json()[key]
    except Exception as e:
        raise e

    return data
