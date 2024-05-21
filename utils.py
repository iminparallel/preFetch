import requests


def get_asset_data( curr: str) -> dict:
    url = "https://api.coinbase.com/api/v3/brokerage/market/products/"
    urlx = url + curr
    response = requests.get(urlx)
    return response.json()