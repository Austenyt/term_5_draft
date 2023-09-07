import psycopg2


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost", database="hh_job",
            user="postgres", password="2so1lTrf6JY-"
        )

    def fill_tables_from_files(self, hh_data):
        self.cur.execute('CREATE TABLE if NOT EXIST Employers (name VARCHAR(255), id INT PRIMARY KEY)')
        self.cur.execute(
            'CREATE TABLE Vacancies (id VARCHAR(255) PRIMARY KEY, employer_id INT, title VARCHAR(255), salary VARCHAR(255), link VARCHAR(255))')
        self.conn.commit()

        for employer_id, vacancies in hh_data:
            self.cur.execute(f"INSERT INTO Employers (name, id) VALUES ('{employer_name}', {employer_id})")

            self.cur.execute(f"""INSERT INTO Vacancies
                                (id, employer_id, title, salary, link)
                                VALUES ('{vacancy_id}', {employer_id}, '{vacancy_title}', '{vacancy_salary}', '{vacancy_link}')""")
        self.conn.commit()
        print('Data was loaded to the database')