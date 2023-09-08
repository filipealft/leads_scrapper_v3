import mysql.connector

def connect_to_database():
    conn = mysql.connector.connect(
        host='13.59.172.35',
        user='filipe_fortunato',
        password='Colorado13!',
        database='i9_tech',
        port='3306'
    )
    return conn

def check_phone_exists(phone):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = """
        SELECT COUNT(*) FROM leads_raw WHERE phone=%s
    """
    cursor.execute(query, (phone,))
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count > 0


def batch_insert_data(connection, data_list):
    cursor = connection.cursor()

    query = "INSERT IGNORE INTO leads_raw (contact_name, phone, segment) VALUES (%s, %s, 'barbearia')"

    try:
        cursor.executemany(query, data_list)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao inserir dados: {err}")
    finally:
        cursor.close()
