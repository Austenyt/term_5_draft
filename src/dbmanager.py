import psycopg2

class DBManager:
    def __init__(self):
        self.conn = None

    def connect_to_db(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="hh_job",
                user="postgres",
                password="2so1lTrf6JY-"
            )
        except psycopg2.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")

    def close_db_connection(self):
        if self.conn:
            self.conn.close()
            print("Соединение с базой данных закрыто")

    def fill_tables_from_files(self, hh_emp_data):
        self.connect_to_db()  # Подключение к базе данных

        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    'CREATE TABLE IF NOT EXISTS Employers (employer_id SERIAL PRIMARY KEY, employer_name VARCHAR('
                    '255))'
                )
                cur.execute(
                    'CREATE TABLE IF NOT EXISTS Vacancies (vacancy_id VARCHAR(255) PRIMARY KEY, '
                    'vacancy_name VARCHAR(255), vacancy_salary VARCHAR(255), '
                    'vacancy_link VARCHAR(255), employer_id INT REFERENCES Employers(employer_id) NOT NULL)'
                )

                # Очищаем таблицы перед вставкой новых данных
                cur.execute('DELETE FROM Vacancies')
                cur.execute('DELETE FROM Employers')

                for item in hh_emp_data:
                    # Вставляем данные в таблицу Employers
                    cur.execute(
                        'INSERT INTO Employers (employer_id, employer_name) VALUES (%s, %s) ON CONFLICT DO NOTHING',
                        (item['employer_id'], item['employer_name'])
                    )

                    # Вставляем данные в таблицу Vacancies
                    cur.execute(
                        'INSERT INTO Vacancies (vacancy_id, vacancy_name, vacancy_salary, vacancy_link, employer_id) '
                        'VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING',
                        (item['vacancy_id'], item['vacancy_name'], item['vacancy_salary'], item['vacancy_link'],
                         item['employer_id'])
                    )

                self.conn.commit()
                print("Данные успешно добавлены в таблицы")
        except psycopg2.Error as e:
            print(f"Ошибка при добавлении данных в таблицы: {e}")
            self.conn.rollback()
        finally:
            self.close_db_connection()  # Закрытие соединения с базой данных

    def get_companies_and_vacancies_count(self):
        self.connect_to_db()  # Подключение к базе данных

        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    'SELECT Employers.employer_name, COUNT(Vacancies.vacancy_id) AS vacancy_count '
                    'FROM Employers '
                    'LEFT JOIN Vacancies ON Employers.employer_id = Vacancies.employer_id '
                    'GROUP BY Employers.employer_name'
                    'ORDER BY employers.name'
                )
                result = cur.fetchall()
                return result
        except psycopg2.Error as e:
            print(f"Ошибка при получении данных: {e}")
        finally:
            self.close_db_connection()  # Закрытие соединения с базой данных

    def get_all_vacancies(self):
        self.connect_to_db()  # Подключение к базе данных

        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    'SELECT Employers.employer_name, Vacancies.vacancy_name, Vacancies.vacancy_salary, Vacancies.vacancy_link '
                    'FROM Vacancies '
                    'LEFT JOIN Employers ON Vacancies.employer_id = Employers.employer_id'
                )
                result = cur.fetchall()
                return result
        except psycopg2.Error as e:
            print(f"Ошибка при получении данных: {e}")
        finally:
            self.close_db_connection()  # Закрытие соединения с базой данных

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        query = "SELECT AVG(salary) FROM vacancies"

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            avg_salary = cursor.fetchone()[0]

        return avg_salary

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        query = f"SELECT * FROM vacancies WHERE salary > {avg_salary}"

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        return results

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        query = f"SELECT * FROM vacancies WHERE description ILIKE '%{keyword}%'"

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        return results

    def closs_conn(self):
        self.conn.close()