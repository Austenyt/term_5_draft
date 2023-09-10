from src.dbmanager import DBManager
from src.hh import HeadHunter

hh = HeadHunter()
hh.get_vacancies()
hh_data = hh.get_format_and_search_vacancies()

db = DBManager()
db.fill_tables_from_files(hh_data)