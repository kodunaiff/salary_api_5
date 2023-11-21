import os

import requests
from dotenv import load_dotenv

from calculat_salary import count_salaries, predict_rub_salary_sj, create_table


def predict_statistic_salary_hh(languages):
    vacansy_language = {}
    for language in languages:
        page = 0
        pages_number = 100
        city = 1
        page_vacancies = []
        while page < pages_number:
            url = 'https://api.hh.ru/vacancies'
            headers = {
                'User-Agent': '',
            }
            params = {
                'text': f'Программист {language}',
                'area': city,
                'page': page
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            sheet = response.json()
            page_vacancies.append(sheet['items'])
            page += 1
            if page > sheet['pages']:
                break
        vacancy_amount = sheet['found']
        salaries = count_salaries(page_vacancies)
        salaries_amount = sum(salaries)
        salaries_count = len(salaries)
        salary_average = int(salaries_amount / salaries_count) if salaries_count else 0
        language_statistic = {
            "vacancies_found": vacancy_amount,
            "vacancies_processed": salaries_count,
            "average_salary": salary_average
        }
        vacansy_language[language] = language_statistic
    return vacansy_language


def predict_statistic_salary_sj(languages, token_sj):
    vacansy_language = {}
    for language in languages:
        page = 0
        pages_number = 25
        city = 4
        profession_catalog = 33
        vacancies = []

        while page < pages_number:
            url = 'https://api.superjob.ru/2.0/vacancies/'
            headers = {
                'X-Api-App-Id': token_sj,
            }
            payload = {
                'town': city,
                'catalogues': profession_catalog,
                'keyword': language,
                'page': page,
            }
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            sheet = response.json()
            for vacancy in sheet['objects']:
                salary = predict_rub_salary_sj(vacancy)
                if salary:
                    vacancies.append(salary)
            page += 1
        vacancy_amount = sheet['total']
        salaries_amount = sum(vacancies)
        salaries_count = len(vacancies)
        salary_average = int(salaries_amount / salaries_count) if salaries_count else 0
        language_statistic = {
            "vacancies_found": vacancy_amount,
            "vacancies_processed": salaries_count,
            "average_salary": salary_average
        }
        vacansy_language[language] = language_statistic
    return vacansy_language


def main():
    languages = [
        'JavaScript', 'Java', 'Python',
        'Ruby', 'PHP', 'C++',
        'C#', 'C', 'Go', 'Swift',
    ]
    load_dotenv()
    token_sj = os.environ['TOKEN_SJ']
    print(create_table('hh', predict_statistic_salary_hh(languages)))
    print(create_table('sj', predict_statistic_salary_sj(languages, token_sj)))


if __name__ == "__main__":
    main()
