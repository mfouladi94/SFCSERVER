import requests


def get_estimated_delivery_time(order_id):
    api_url = f'https://run.mocky.io/v3/122c2796-5df4-461c-ab75-87c1192b17f7/{order_id}'
    response = requests.get(api_url)
    return response.json().get('estimated_delivery_time')
