import os

import requests
from dotenv import load_dotenv

from calculat_salary import give_salaries, predict_rub_salary_sj, create_table


def give_statistic_hh(languages):
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
            page_request = response.json()
            page_vacancies.append(page_request['items'])
            page += 1
            if page > page_request['pages']:
                break
        vacancy_amount = page_request['found']
        salaries = give_salaries(page_vacancies)
        salary_average = int(sum(salaries) / len(salaries))
        language_statistic = {
            "vacancies_found": vacancy_amount,
            "vacancies_processed": len(salaries),
            "average_salary": salary_average
        }
        vacansy_language[language] = language_statistic
    return vacansy_language


def give_statistic_sj(languages, token_sj):
    vacansy_language = {}
    for language in languages:
        page = 0
        pages_number = 25
        city = 4
        profession_catalog = 33
        vacancies = []
        vacancies_all = []

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
            page_request = response.json()
            for vacancy in page_request['objects']:
                salary = predict_rub_salary_sj(vacancy)
                if salary:
                    vacancies.append(salary)
                vacancies_all.append((vacancy['profession']))
            page += 1
        salary_average = sum(vacancies)
        if len(vacancies) > 0:
            language_statistic = {
                "vacancies_found": len(vacancies_all),
                "vacancies_processed": len(vacancies),
                "average_salary": int(salary_average / len(vacancies))
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
    print(create_table('hh', give_statistic_hh(languages)))
    print(create_table('sj', give_statistic_sj(languages, token_sj)))


if __name__ == "__main__":
    main()
