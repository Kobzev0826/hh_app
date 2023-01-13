import os
import requests
import dotenv
from terminaltables import AsciiTable
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
    all_data = {}
    all_data["items"]=[]
    all_data["found"] = 0
    while more :
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()

        all_data['found'] = response.json()['total']
        all_data["items"] += response.json()['objects']
        # print(f'{len(all_data["items"])}/ {all_data["found"]}')
        page += 1
        payload ['page'] = page
        more = response.json()['more']

    return all_data


def predict_rub_salary_for_superJob(vacancy):
    # print (vacancy)
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return 1.2 * salary_from
    if salary_to:
        return 0.8 * salary_to
    return None


# def get_sallary(records):
#     processed = 0
#     mid_salary = 0
#     for vacancy in records['items']:
#         salary = predict_rub_salary_for_superJob(vacancy)
#         if salary:
#             mid_salary+=salary
#             processed+=1
#     mid_salary /= processed
#     return mid_salary, processed


# def get_sallary_by_language(language):
#     records = get_found_records(language)
#     mid_salary, processed =get_sallary(records)
#     # return {
#     #     "vacancies_found": records['found'],
#     #     "vacancies_processed": processed,
#     #     "average_salary": mid_salary
#     # }
#     return [language, records['found'],processed, mid_salary ]



# if __name__ == '__main__':
#     dotenv.load_dotenv()
#     popular_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go']
#     # vacancies_by_language = {}
#     table_data = [
#         ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', "Средняя зарплата"],
#     ]
#     for language in popular_languages:
#         # vacancies_by_language[language] = get_sallary_by_language(language)
#         table_data.append(get_sallary_by_language(language))

    # print(vacancies_by_language)


    table = AsciiTable(table_data, 'SuperJob.ru')
    print(table.table)

    # for vacancy in get_vacancyes('Программист'):
    #     salary = predict_rub_salary_for_superJob(vacancy)
    #     print(f"{vacancy['profession']}, {vacancy['town']['title']}, salary = {salary}")