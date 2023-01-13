import requests


def get_found_records(text="", days=0):
    url = 'https://api.hh.ru/vacancies'
    payload ={
        'professional_role': 96,
        'area': 1,
        'per_page':100,
        'text':text
    }
    if days != 0:
        payload['period'] = days

    response = requests.get(url,params=payload)
    response.raise_for_status()
    # all_data={}
    all_data = response.json()

    pages = response.json()['pages']
    for page in range(1,pages):
        # print(f'page {page}')
        payload['page'] = page
        response = requests.get(url, params=payload)
        response.raise_for_status()
        all_data["items"] += response.json()["items"]
        # print(f'data size : {len(all_data["items"])} ')
    return all_data


def predict_rub_salary(vacancy):
    salary = vacancy['salary']
    if not salary or salary['currency'] != 'RUR':
        return None

    salary_from = salary['from']
    salary_to = salary['to']
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return 1.2 * salary_from
    if salary_to:
        return 0.8 * salary_to

