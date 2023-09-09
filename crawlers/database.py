import mysql.connector

def connect_to_database():
    conn = mysql.connector.connect(
        host='3.143.204.99',
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

def fetch_urls_from_database():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT url_link FROM url WHERE status IS NULL OR status != 'captado'"
    cursor.execute(query)
    urls = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return urls

def mark_url_as_captured(url_link):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "UPDATE url SET status = 'captado' WHERE url_link = %s"
    cursor.execute(query, (url_link,))
    connection.commit()
    cursor.close()
    connection.close()
