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
        print(json.dumps(self.vacancies, indent=4, ensure_ascii=True))

    def get_format_and_search_vacancies(self):
        hh_emp_data = []
        for vacancy in self.vacancies:
            if vacancy["employer"]["id"] in [1122462, 6, 78638]:
                hh_emp_data.append(
                    {
                    'vacancy_id': vacancy['id'],
                    'vacancy_title': vacancy['name'],
                    'vacancy_salary': vacancy.get('salary', {}).get('from'),
                    'vacancy_link': vacancy['alternate_url'],
                    'employer_id': vacancy["employer"]["id"]
                    }
                )
        return hh_emp_data
