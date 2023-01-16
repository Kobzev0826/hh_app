import requests
from main import calc_salary

def get_found_records(query="", days=0,professional_role = 96, area = 1, per_page = 100,secret_key = ""):
    url = 'https://api.hh.ru/vacancies'
    payload = {
        'professional_role': professional_role,
        'area': area,
        'per_page': per_page,
        'text': query
    }
    if days:
        payload['period'] = days

    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()

    all_pages_response = response

    pages = response['pages']
    for page in range(1, pages):
        payload['page'] = page
        response = requests.get(url, params=payload)
        response.raise_for_status()
        all_pages_response["items"] += response.json()["items"]
    return all_pages_response


def predict_rub_salary(vacancy):
    salary = vacancy['salary']
    if not salary or salary['currency'] != 'RUR':
        return None
    return calc_salary(salary['from'], salary['to'])

