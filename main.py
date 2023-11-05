import os

import requests
from dotenv import load_dotenv

from func_main import sum_salary, predict_rub_salary_sj, vacansy_table


def headhunter_vacansy(languages):
    vacansy_language = {}
    for language in languages:
        page = 0
        pages_number = 100
        vacancies = []
        while page < pages_number:
            url = 'https://api.hh.ru/vacancies'
            headers = {
                'User-Agent': '',
            }
            params = {
                'text': f'Программист {language}',
                'area': '1',
                'page': page
            }
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            vacancy = response.json().get('items')
            vacancies.append(vacancy)
            page += 1
            page_number = response.json().get('pages')
            if page > page_number:
                break
        vacancy_amount = response.json().get('found')
        salary_count = sum_salary(vacancies)
        salary_average = int(sum(salary_count) / len(salary_count))
        language_info = {
            "vacancies_found": vacancy_amount,
            "vacancies_processed": len(salary_count),
            "average_salary": salary_average
        }
        vacansy_language[language] = language_info
    return vacansy_language


def superjob_vacansy(languages, token_sj):
    vacansy_language = {}
    for language in languages:
        page = 0
        pages_number = 25
        vacancies = []
        vacancies_all = []

        while page < pages_number:
            url = 'https://api.superjob.ru/2.0/vacancies/'
            headers = {
                'X-Api-App-Id': token_sj,
            }
            payload = {
                'town': 4,
                'catalogues': 33,
                'keyword': language,
                'page': page,
            }
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            vacancy = response.json().get('objects')
            for items in vacancy:
                vac = predict_rub_salary_sj(items)
                if vac:
                    vacancies.append(vac)
                vacancies_all.append((items['profession']))
            page += 1
        salary_average = sum(vacancies)
        if len(vacancies) > 0:
            language_info = {
                "vacancies_found": len(vacancies_all),
                "vacancies_processed": len(vacancies),
                "average_salary": int(salary_average / len(vacancies))
            }
            vacansy_language[language] = language_info
    return vacansy_language


def main():
    languages = [
        'JavaScript', 'Java', 'Python',
        'Ruby', 'PHP', 'C++',
        'C#', 'C', 'Go', 'Swift',
    ]
    load_dotenv()
    token_sj = os.environ['TOKEN_SJ']
    print(vacansy_table('hh', headhunter_vacansy(languages)))
    print(vacansy_table('sj', superjob_vacansy(languages, token_sj)))


if __name__ == "__main__":
    main()
