from terminaltables import AsciiTable


def create_table(title, statistic_vacansy):
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
