import csv


class DBManager:
    def __init__(self, conn_obj):
        self.conn = conn_obj
        self.cursor = self.conn.cursor()

    @staticmethod
    def get_data_from_csv(filename):
        """
        Чтение данных из CSV
        """
        data = []
        with open(filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
                data.append(cleaned_row)
        return data

    def insert_one(self, table_name, **data):
        """
        Вставка одной записи с использованием параметризованного запроса
        по ключам раскидываем плейсхолдеры, потом отдельно закидываем параметры
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        SQL_QUERY = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            self.cursor.execute(SQL_QUERY, tuple(data.values()))
            self.conn.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def insert_all(self, filename, table_name):
        """
        Вставка всех записей из CSV
        """
        data_to_insert = DBManager.get_data_from_csv(filename)
        print(f"  Найдено записей: {len(data_to_insert)}")

        if data_to_insert:
            print(f"  Первая запись: {data_to_insert[0]}")

        success_count = 0
        for data in data_to_insert:
            if self.insert_one(table_name, **data):
                success_count += 1
        print(f'Данные помещены в таблицу {table_name}. Успешно: {success_count} из {len(data_to_insert)}')

    def insert_employees_from_csv(self, filename, start_id=1):
        """
        Вставка сотрудников из CSV с добавлением ID
        """
        data_to_insert = DBManager.get_data_from_csv(filename)
        print(f"  Найдено записей: {len(data_to_insert)}")

        if data_to_insert:
            print(f"  Первая запись: {data_to_insert[0]}")

        success_count = 0
        for idx, data in enumerate(data_to_insert, start=start_id):
            data['employee_id'] = idx
            if self.insert_one('employees_data', **data):
                success_count += 1
        print(f'Данные помещены в таблицу employees_data. Успешно: {success_count} из {len(data_to_insert)}')

    def select(self, table_name, **conditions):
        """
        По запросу получаем данные из бд в ввиде списка картжей, либо None если в бд нет
        """
        try:
            query = f'SELECT * FROM {table_name}'
            if conditions:
                query += ' WHERE ' + ' AND '.join([f'{col} = ?' for col in conditions.keys()])
                self.cursor.execute(query, tuple(conditions.values()))
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as ex:
            print(f"Ошибка SELECT: {ex}")
            return None

    def update(self, table_name, set_data, **conditions):
        """
        Обновляем данные в DB
        """
        try:
            set_clause = ', '.join([f'{col} = ?' for col in set_data.keys()])
            query = f'UPDATE {table_name} SET {set_clause}'
            if conditions:
                query += ' WHERE ' + ' AND '.join([f'{col} = ?' for col in conditions.keys()])
                params = tuple(list(set_data.values()) + list(conditions.values()))
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query, tuple(set_data.values()))
            self.conn.commit()
            print('Запрос UPDATE успешно выполнен')
        except Exception as ex:
            print(f"Ошибка UPDATE: {ex}")

    def delete(self, table_name, **conditions):
        """
        Удаляем данные и DB
        """
        try:
            query = f'DELETE FROM {table_name}'
            if conditions:
                query += ' WHERE ' + ' AND '.join([f'{col} = ?' for col in conditions.keys()])
                self.cursor.execute(query, tuple(conditions.values()))
            else:
                self.cursor.execute(query)
            self.conn.commit()
            print('Запрос DELETE успешно выполнен')
        except Exception as ex:
            print(f"Ошибка DELETE: {ex}")

    def execute_query_cursor(self, SQL_QUERY):
        """
        метод для выполнения запросов, с перехватом ошибок
        """
        try:
            self.cursor.execute(SQL_QUERY)
            self.conn.commit()
            return True
        except Exception as ex:
            print(f"Ошибка выполнения запроса: {ex}")
            return False