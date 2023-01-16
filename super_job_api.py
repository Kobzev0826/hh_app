import os
import requests
from main import calc_salary


def get_found_records(query = "", secret_key = ""):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret_key
    }
    payload = {
        'town': 'Moscow',
        'keyword': query,
        'count': 100
    }
    page = 0
    more = True
    all_pages_response = {"items": [], "found": 0}

    while more:
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        response_json = response.json()

        all_pages_response = {
            'found' : response_json['total'],
            'items' : all_pages_response['items']+response_json['objects']
        }

        page += 1
        payload['page'] = page
        more = response_json['more']

    return all_pages_response


def predict_rub_salary_for_superJob(vacancy):
    return calc_salary(vacancy['payment_from'], vacancy['payment_to'])

