import super_job_api, hh_app
import dotenv
from terminaltables import AsciiTable


def get_sallary(records, predict_func):
    processed = 0
    mid_salary = 0
    for vacancy in records['items']:
        salary = predict_func(vacancy)
        if salary:
            mid_salary+=salary
            processed+=1
    mid_salary /= processed
    return mid_salary, processed


def get_sallary_by_language(language, found_records, predict_func):
    records = found_records(language)
    mid_salary, processed =get_sallary(records,predict_func)
    return [language, records['found'],processed, mid_salary ]


if __name__ == '__main__':
    dotenv.load_dotenv()
    popular_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go']
    table_data_superjob = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', "Средняя зарплата"],
    ]
    table_data_hh = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', "Средняя зарплата"],
    ]
    for language in popular_languages:
        # vacancies_by_language[language] = get_sallary_by_language(language)
        table_data_superjob.append(get_sallary_by_language(language, super_job_api.get_found_records, super_job_api.predict_rub_salary_for_superJob))
        table_data_hh.append(get_sallary_by_language(language, hh_app.get_found_records, hh_app.predict_rub_salary))

    table_superjob = AsciiTable(table_data_superjob, 'SuperJob.ru')
    table_hh = AsciiTable(table_data_hh, 'HeadHunter.ru')
    print(table_superjob.table)
    print(table_hh.table)
