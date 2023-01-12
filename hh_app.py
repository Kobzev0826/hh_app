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


def get_sallary(records):
    processed = 0
    mid_salary = 0
    for vacancy in records['items']:
        salary = predict_rub_salary(vacancy)
        if salary:
            mid_salary+=salary
            processed+=1
    mid_salary /= processed
    return mid_salary, processed


def get_sallary_by_language(language):
    records = get_found_records(language)
    mid_salary, processed =get_sallary(records)
    return {
        "vacancies_found": records['found'],
        "vacancies_processed": processed,
        "average_salary": mid_salary
    }

# print(f'vacansies in Moscow last 30 days = {get_found_records(30)}')
# print(f'vacansies in Moscow all time = {get_found_records()}')
#
popular_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++','C#', 'C', 'Go' ]
vacancies_by_language={}
for language in popular_languages:
    vacancies_by_language[language] = get_sallary_by_language(language)
print(vacancies_by_language)

# get_sallary_by_language('Python')

# print(get_sallary_by_language("Python"))