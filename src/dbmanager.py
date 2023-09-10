import psycopg2



class DBManager:
    def __init__(self):
        self.conn = None

    def fill_tables_from_files(self, hh_emp_data):
        try:
            with psycopg2.connect(
                host="localhost",
                database="hh_job",
                user="postgres",
                password="2so1lTrf6JY-"
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        'CREATE TABLE IF NOT EXISTS Employers (employer_id SERIAL PRIMARY KEY, employer_name VARCHAR('
                        '255))'
                    )
                    cur.execute(
                        'CREATE TABLE IF NOT EXISTS Vacancies (vacancy_id VARCHAR(255) PRIMARY KEY, '
                        'vacancy_name VARCHAR(255), vacancy_salary VARCHAR(255), '
                        'vacancy_link VARCHAR(255), employer_id INT REFERENCES Employers(employer_id) NOT NULL)'
                )

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

                    conn.commit()
                    print("Данные успешно добавлены в таблицы")
        except psycopg2.Error as e:
            print(f"Ошибка при добавлении данных в таблицы: {e}")
            conn.rollback()
        finally:
            if conn:
                conn.close()
                print("Соединение с базой данных закрыто")
