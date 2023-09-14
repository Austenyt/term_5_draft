import json
from abc import ABC, abstractmethod
import requests


class API_abstract(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunter(API_abstract):

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies/"

    def get_vacancies(self, text='python'):
        params = {
            'text': f"NAME:{text}",  # Текст фильтра. В имени должно быть слово "Python"
            'area': 1,  # Поиск оcуществляется по вакансиям города Москва
            'page': 0,  # Индекс страницы поиска на HH
            'per_page': '100'  # Кол-во вакансий на 1 странице

        }
        response = requests.get(self.url, params)
        self.vacancies = response.json()['items']
        # print(self.vacancies)
        # print(json.dumps(self.vacancies, indent=4, ensure_ascii=True))

    # def get_format_and_search_vacancies(self):
    #     hh_emp_data = []
    #     for vacancy in self.vacancies:
    #         if vacancy["employer"]["id"] in [5781952]: #4934622, 699283, 9150066, 5788049, 9501038, 59645, 3368301, 47479, 2760901]:
    #             hh_emp_data.append(
    #                 {
    #                 'vacancy_id': vacancy['id'],
    #                 'vacancy_title': vacancy['name'],
    #                 'vacancy_salary': vacancy.get('salary', {}).get('from'),
    #                 'vacancy_link': vacancy['alternate_url'],
    #                 'employer_id': vacancy["employer"]["id"]
    #                 }
    #             )
    #     print(hh_emp_data)

    def get_format_and_search_vacancies(self):
        # Получение информации о работодателях из переменной self.vacancies без повторений
        hh_emp_data = []
        seen_employers = set()  # Множество для отслеживания уже добавленных работодателей

        for vacancy in self.vacancies[:11]:
            employer_info = vacancy.get('employer', {})
            employer_id = employer_info.get('id')
            if employer_id not in seen_employers:
                salary_info = vacancy.get('salary', {})
                vacancy_salary = salary_info.get('from', 'Не указано') if salary_info else 'Не указано'
                emp_info = {
                    'employer_name': employer_info.get('name', 'Не указано'),
                    'employer_id': employer_id,
                    'vacancy_name': vacancy.get('name', 'Не указано'),
                    'vacancy_id': vacancy.get('id', 'Не указано'),
                    'vacancy_salary': vacancy_salary,
                    'vacancy_link': vacancy.get('alternate_url', 'Не указано'),
                }
                hh_emp_data.append(emp_info)
                seen_employers.add(employer_id)

        return hh_emp_data
