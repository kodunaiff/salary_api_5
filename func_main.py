from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return salary_from * 1.2
    if salary_to:
        return salary_to * 0.8


def predict_rub_salary(vacancy):
    if vacancy and vacancy['currency'] == 'RUR':
        salary_from = vacancy['from']
        salary_to = vacancy['to']
        return predict_salary(salary_from, salary_to)


def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] == 'rub':
        salary_from = vacancy['payment_from']
        salary_to = vacancy['payment_to']
        return predict_salary(salary_from, salary_to)


def sum_salary(vacancies):
    salaries = []
    for vacancy in vacancies:
        for items in vacancy:
            salary_zp = predict_rub_salary(items['salary'])
            if salary_zp:
                salaries.append(salary_zp)
    return salaries


def vacansy_table(title, statistic_vacansy):
    table_headers = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
    ]
    table = [
        table_headers,
    ]
    for lang, params in statistic_vacansy.items():
        table_raw = [
            lang,
            params['vacancies_found'],
            params['vacancies_processed'],
            params['average_salary'],
        ]
        table.append(table_raw)
    table = AsciiTable(table, title)
    return table.table
