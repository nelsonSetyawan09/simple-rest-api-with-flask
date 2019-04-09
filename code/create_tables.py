import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='moliASroot09',
                             db='test_flask',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        users_table= """CREATE TABLE IF NOT EXISTS users (
                        id INT NOT NULL AUTO_INCREMENT,
                        username VARCHAR(255)  NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL,
                        PRIMARY KEY (`id`))"""

        cursor.execute(users_table)

        stores_table= """CREATE TABLE IF NOT EXISTS stores (
                        id INT NOT NULL AUTO_INCREMENT,
                        name VARCHAR(255)  NOT NULL UNIQUE,
                        PRIMARY KEY (`id`));
                        """
        cursor.execute(stores_table)

        items_table= """CREATE TABLE IF NOT EXISTS items (
                        id INT NOT NULL AUTO_INCREMENT,
                        name VARCHAR(255)  NOT NULL UNIQUE,
                        price DECIMAL(6,2) NOT NULL,
                        PRIMARY KEY (`id`));
                        """
        cursor.execute(items_table)


finally:
    connection.close()
