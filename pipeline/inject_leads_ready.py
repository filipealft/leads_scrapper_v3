import mysql.connector

def connect_to_database():
    conn = mysql.connector.connect(
        host='18.119.110.40',
        user='filipe_fortunato',
        password='Colorado13!',
        database='i9_tech',
        port='3306'
    )
    return conn


def inject_leads():
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    INSERT INTO leads_ready (contact_name, phone, status)
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