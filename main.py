import super_job_api, hh_app
import dotenv
from terminaltables import AsciiTable


def calc_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return 1.2 * salary_from
    if salary_to:
        return 0.8 * salary_to
    return None


def get_sallary(records, predict_func):
    processed = 0
    mid_salary = 0
    for vacancy in records['items']:
        salary = predict_func(vacancy)
        if salary:
            mid_salary += salary
            processed += 1
    if processed:
        mid_salary /= processed

    return mid_salary, processed


def get_language_statistics(language, found_records, predict_func):
    vacancies = found_records(language)
    mid_salary, processed = get_sallary(vacancies, predict_func)
    return [language, vacancies['found'], processed, mid_salary]


if __name__ == '__main__':
    dotenv.load_dotenv()
    popular_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go']
    table_superjob = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', "Средняя зарплата"],
    ]
    table_hh = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', "Средняя зарплата"],
    ]
    for language in popular_languages:
        table_superjob.append(get_language_statistics(language, super_job_api.get_found_records,
                                                      super_job_api.predict_rub_salary_for_superJob))
        table_hh.append(get_language_statistics(language, hh_app.get_found_records, hh_app.predict_rub_salary))

    print(AsciiTable(table_superjob, 'SuperJob.ru').table)
    print(AsciiTable(table_hh, 'HeadHunter.ru').table)
