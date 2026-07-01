import os
from dotenv import load_dotenv

from operator_db import ConnectDB, MSSQLOperator
from manager_db import DBManager
import SQLQueries as SQL



if __name__ == '__main__':
    load_dotenv()

    DRIVER = os.getenv('MS_SQL_DRIVER')
    SERVER = os.getenv('MS_SQL_SERVER')
    DATABASE = 'NorthWind'
    USER = os.getenv('MS_SQL_USER')
    PASSWORD = os.getenv('MS_SQL_KEY')
    PAD_DATABASE = os.getenv('MS_SQL_PAD_DATABASE')


    """
    Создание DB
    """
    print("\nСоздание базы данных...")
    pad_conn = ConnectDB.connect_to_db(DRIVER, SERVER, PAD_DATABASE, USER, PASSWORD)
    if pad_conn is None:
        print("Не удалось подключиться")
        exit(1)

    pad_operator = MSSQLOperator(pad_conn, PAD_DATABASE)
    pad_operator.create_database(DATABASE)
    pad_conn.close()

    """
    Подключение к DB
    """
    print("\nПодключение к базе данных...")
    main_conn = ConnectDB.connect_to_db(DRIVER, SERVER, DATABASE, USER, PASSWORD)
    if main_conn is None:
        print(f"Не удалось подключиться к БД {DATABASE}")
        exit(1)
    else:
        print('Подключение успешно.')

    main_operator = MSSQLOperator(main_conn, DATABASE)

    """
    Создание таблиц в DB
    """
    print("\nСоздание таблиц...")
    main_operator.drop_table('orders_data')
    main_operator.drop_table('customers_data')
    main_operator.drop_table('employees_data')

    main_operator.cursor.execute(SQL.CREATE_CUSTOMERS_TABLE)
    main_operator.cursor.execute(SQL.CREATE_EMPLOYEES_TABLE)
    main_operator.cursor.execute(SQL.CREATE_ORDERS_TABLE)
    main_operator.conn.commit()
    print("Все таблицы успешно созданы")

    """
    Заполнение таблиц
    """
    print()
    db_manager = DBManager(main_conn)
    print("\nЗагрузка customers_data из customers_data.csv:")
    db_manager.insert_all('data/customers_data.csv', 'customers_data')

    print("\nЗагрузка employees_data из employees_data.csv (с добавлением ID):")
    db_manager.insert_employees_from_csv('data/employees_data.csv', start_id=1)

    print("\nЗагрузка orders_data из orders_data.csv:")
    db_manager.insert_all('data/orders_data.csv', 'orders_data')

    """
    Получение данных с условием
    """
    print()

    print("\nЗаказы в городе Berlin:")
    result = db_manager.select('orders_data', ship_city='Berlin')
    if result:
        for row in result:
            print(f"  Заказ #{row[0]}: клиент {row[1]}, сотрудник {row[2]}, {row[3]}, {row[4]}")
    else:
        print("  Нет заказов в Berlin")

    print("\nСотрудники с должностью 'Sales Representative':")
    result = db_manager.select('employees_data', title='Sales Representative')
    if result:
        for row in result:
            print(f"  {row[0]}: {row[1]} {row[2]} - {row[3]}")
    else:
        print("  Нет сотрудников с такой должностью")

    print("\nКлиент с ID 'ALFKI':")
    result = db_manager.select('customers_data', customer_id='ALFKI')
    if result:
        for row in result:
            print(f"  {row[0]}: {row[1]} ({row[2]})")
    else:
        print("  Клиент не найден")

    """
    Изменение записей
    """
    print("\n7. Изменение записи (UPDATE):")
    print()

    print("\nОбновление города в заказе #10248 на 'Bonn':")
    db_manager.update('orders_data', {'ship_city': 'Bonn'}, order_id=10248)

    result = db_manager.select('orders_data', order_id=10248)
    if result:
        for row in result:
            print(f"  Заказ #{row[0]}: новый город - {row[4]}")

    print("\nОбновление должности сотрудника #1 на 'Senior Sales Representative':")
    db_manager.update('employees_data', {'title': 'Senior Sales Representative'}, employee_id=1)

    result = db_manager.select('employees_data', employee_id=1)
    if result:
        for row in result:
            print(f"  {row[0]}: {row[1]} {row[2]} - {row[3]}")

    """
    Удаление записи
    """
    print("\n8. Удаление записи (DELETE):")
    print()

    print("\nУдаление заказа #10252:")
    db_manager.delete('orders_data', order_id=10252)

    result = db_manager.select('orders_data', order_id=10252)
    if not result:
        print("  Заказ #10252 успешно удален")

    print("\nУдаление заказов клиента 'ANTON':")
    db_manager.delete('orders_data', customer_id='ANTON')

    result = db_manager.select('orders_data', customer_id='ANTON')
    if not result:
        print("  Заказ клиента ANTON успешно удален")

    print("\nУдаление клиента 'ANTON':")
    db_manager.delete('customers_data', customer_id='ANTON')

    result = db_manager.select('customers_data', customer_id='ANTON')
    if not result:
        print("  Клиент ANTON успешно удален")

    

    main_conn.close()

