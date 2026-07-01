"""
комадны на создание таблиц
"""
CREATE_CUSTOMERS_TABLE = '''
CREATE TABLE customers_data (
    customer_id NVARCHAR(10) PRIMARY KEY,
    company_name NVARCHAR(100) NOT NULL,
    contact_name NVARCHAR(50) NOT NULL
)
'''

CREATE_EMPLOYEES_TABLE = '''
CREATE TABLE employees_data (
    employee_id INT PRIMARY KEY,
    first_name NVARCHAR(100) NOT NULL,
    last_name NVARCHAR(100) NOT NULL,
    title NVARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    notes NVARCHAR(1000) NOT NULL
)
'''

CREATE_ORDERS_TABLE = '''
CREATE TABLE orders_data (
    order_id INT PRIMARY KEY,
    customer_id NVARCHAR(10) NOT NULL,
    employee_id INT NOT NULL,
    order_date DATE NOT NULL,
    ship_city NVARCHAR(100) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers_data(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees_data(employee_id)
)
'''