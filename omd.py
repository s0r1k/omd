import argparse
import csv
from pathlib import Path


INPUT_FILE = Path(__file__).resolve().parent / 'Corp_Summary.csv'
OUTPUT_FILE = Path(__file__).resolve().parent / 'department_summary.csv'


def read_employees(filename):
    """Прочитать сотрудников из CSV-файла."""
    employees = []

    with open(filename, 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader, None)

        for row in reader:
            if not row:
                continue

            employees.append({
                'department': row[1],
                'team': row[2],
                'salary': int(row[5]),
            })

    return employees


def show_hierarchy(employees):
    """Вывести команды каждого департамента."""
    departments = {}

    for employee in employees:
        department = employee['department']

        if department not in departments:
            departments[department] = set()

        departments[department].add(employee['team'])

    for department in sorted(departments):
        print(department)

        for team in sorted(departments[department]):
            print(f'  - {team}')

        print()


def calculate_summary(employees):
    """Рассчитать количество сотрудников и статистику окладов."""
    department_salaries = {}

    for employee in employees:
        department = employee['department']

        if department not in department_salaries:
            department_salaries[department] = []

        department_salaries[department].append(employee['salary'])

    summary = []

    for department in sorted(department_salaries):
        salaries = department_salaries[department]

        summary.append({
            'department': department,
            'count': len(salaries),
            'minimum': min(salaries),
            'maximum': max(salaries),
            'average': sum(salaries) / len(salaries),
        })

    return summary


def show_summary(employees):
    """Вывести сводку по департаментам на экран."""
    summary = calculate_summary(employees)

    for department_stats in summary:
        department = department_stats['department']
        count = department_stats['count']
        minimum = department_stats['minimum']
        maximum = department_stats['maximum']
        average = department_stats['average']

        print(department)
        print(f'  Сотрудников: {count}')
        print(f'  Минимальный оклад: {minimum}')
        print(f'  Максимальный оклад: {maximum}')
        print(f'  Средний оклад: {average:.2f}')
        print()


def save_summary(employees, filename):
    """Сохранить сводку по департаментам в CSV."""
    summary = calculate_summary(employees)

    with open(filename, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        writer.writerow([
            'Департамент',
            'Количество сотрудников',
            'Минимальный оклад',
            'Максимальный оклад',
            'Средний оклад',
        ])

        for department_stats in summary:
            average = department_stats['average']

            writer.writerow([
                department_stats['department'],
                department_stats['count'],
                department_stats['minimum'],
                department_stats['maximum'],
                f'{average:.2f}',
            ])

    print(f'Отчёт сохранён: {filename}')


def main(variant: int, input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    """Прочитать данные и сформировать выбранный отчёт."""
    if variant not in (1, 2, 3):
        raise ValueError('Номер отчёта должен быть 1, 2 или 3')

    employees = read_employees(input_file)

    if variant == 1:
        show_hierarchy(employees)
    elif variant == 2:
        show_summary(employees)
    else:
        save_summary(employees, output_file)


def parse_arguments():
    """Получить номер отчёта из командной строки."""
    parser = argparse.ArgumentParser(
        description='Отчёты по сотрудникам компании'
    )
    parser.add_argument(
        'variant',
        type=int,
        choices=[1, 2, 3],
        help='1 - иерархия, 2 - сводка, 3 - сохранение сводки в CSV',
    )
    return parser.parse_args()


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.variant)