import os
import requests

def get_found_records(keyword):

    Secret_Key = os.environ['SuperJob']
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers ={
            'X-Api-App-Id' : Secret_Key
        }
    payload ={
    'town': 'Moscow',
        'keyword': keyword,
        'count' : 100
    }
    page = 0
    more = True
    all_pages_response = {}
    all_pages_response["items"]=[]
    all_pages_response["found"] = 0

    while more :
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()

        all_pages_response['found'] = response.json()['total']
        all_pages_response["items"] += response.json()['objects']
        page += 1
        payload ['page'] = page
        more = response.json()['more']

    return all_pages_response


def predict_rub_salary_for_superJob(vacancy):

    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return 1.2 * salary_from
    if salary_to:
        return 0.8 * salary_to
    return None

