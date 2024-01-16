import mysql.connector

def connect_to_database():
    conn = mysql.connector.connect(
        host='',
        user='',
        password='',
        database='',
        port=''
    )
    return conn


def inject_leads():
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
        INSERT IGNORE INTO leads_ready (contact_name, phone, status)
        SELECT contact_name, phone, 'stand by'
        FROM leads_raw
        WHERE SUBSTRING(phone, 3, 1) != '3';

    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    inject_leads()
