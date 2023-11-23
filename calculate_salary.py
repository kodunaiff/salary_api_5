def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return salary_from * 1.2
    if salary_to:
        return salary_to * 0.8


def predict_rub_salary(vacancy):
    if not vacancy or vacancy['currency'] != 'RUR':
        return None
    return predict_salary(vacancy['from'], vacancy['to'])


def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] != 'rub':
        return None
    return predict_salary(vacancy['payment_from'], vacancy['payment_to'])


def count_salaries(page_vacancies):
    salaries = []
    for vacancy in page_vacancies:
        salary = predict_rub_salary(vacancy['salary'])
        if salary:
            salaries.append(salary)
    return salaries
