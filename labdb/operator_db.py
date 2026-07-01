import pyodbc


class ConnectDB:
    @classmethod
    def connect_to_db(cls, driver, server, database, user, password, param=True):
        """
        Подключение
        """
        if database is None or database == 'None':
            print(f"Ошибка: database = {database}")
            return None

        ConnectionString = f"""DRIVER={driver};
                            SERVER={server};
                            DATABASE={database};
                            UID={user};
                            PWD={password};
                            Encrypt=no;
                            TrustServerCertificate=yes;"""
        try:
            conn = pyodbc.connect(ConnectionString)
            conn.autocommit = param
        except pyodbc.Error as ex:
            print(ex)
            return None
        else:
            return conn


class MSSQLOperator:
    """
    основные операции, создание, дроп, выполнение
    """
    def __init__(self, conn_obj, database_name):
        self.conn = conn_obj
        self.cursor = self.conn.cursor()
        self.database_name = database_name

    def create_database(self, database_name):
        SQL_QUERY = fr"CREATE DATABASE {database_name};"
        return self.execute_query_conn(SQL_QUERY)

    def drop_database(self, database_name):
        SQL_QUERY = fr"DROP DATABASE {database_name};"
        return self.execute_query_conn(SQL_QUERY)

    def create_table(self, table_name, **columns):
        columns_with_types = ', '.join([f'{col} {dtype}' for col, dtype in columns.items()])
        SQL_QUERY = f'CREATE TABLE {table_name} ({columns_with_types})'
        return self.execute_query_cursor(SQL_QUERY)

    def drop_table(self, table_name):
        SQL_QUERY = fr"DROP TABLE {table_name};"
        return self.execute_query_cursor(SQL_QUERY)

    def execute_query_conn(self, SQL_QUERY):
        try:
            self.conn.execute(SQL_QUERY)
        except pyodbc.Error as ex:
            print(ex)
            return False
        else:
            print(f'Запрос успешно выполнен')
            return True

    def execute_query_cursor(self, SQL_QUERY):
        try:
            self.cursor.execute(SQL_QUERY)
        except pyodbc.Error as ex:
            print(ex)
            return False
        else:
            print(f'Запрос успешно выполнен')
            return True

