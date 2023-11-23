import os

import requests
from dotenv import load_dotenv

from calculate_salary import count_salaries, predict_rub_salary_sj
from create_table import create_table


def predict_statistic_salary_hh(languages):
    language_statistic = {}
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
            page_vacancies.extend(sheet['items'])
            page += 1
            if page > sheet['pages']:
                break
        vacancy_amount = sheet['found']
        salaries = count_salaries(page_vacancies)
        salaries_amount = sum(salaries)
        salaries_count = len(salaries)
        average_salary = int(salaries_amount / salaries_count) if salaries_count else 0
        statistic = {
            "vacancies_found": vacancy_amount,
            "vacancies_processed": salaries_count,
            "average_salary": average_salary
        }
        language_statistic[language] = statistic
    return language_statistic


def predict_statistic_salary_sj(languages, token_sj):
    language_statistic = {}
    for language in languages:
        page = 0
        pages_number = 25
        city = 4
        profession_catalog = 33
        salaries = []

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
                    salaries.append(salary)
            page += 1
        vacancy_amount = sheet['total']
        salaries_amount = sum(salaries)
        salaries_count = len(salaries)
        average_salary = int(salaries_amount / salaries_count) if salaries_count else 0
        statistic = {
            "vacancies_found": vacancy_amount,
            "vacancies_processed": salaries_count,
            "average_salary": average_salary
        }
        language_statistic[language] = statistic
    return language_statistic


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
