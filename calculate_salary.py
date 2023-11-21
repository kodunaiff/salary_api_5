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


def count_salaries(page_vacancies):
    salaries = []
    for vacancy in page_vacancies:
        salary = predict_rub_salary(vacancy['salary'])
        if salary:
            salaries.append(salary)
    return salaries
