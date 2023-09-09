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

def get_phone_leads_ready():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = """
        SELECT phone FROM leads_ready WHERE status = 'stand by'
    """
    cursor.execute(query)
    data = [item[0] for item in cursor.fetchall()]
    cursor.close()
    connection.close()
    return data


def update_lead_status_to_captured(phone):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = """
        UPDATE leads_ready SET status = 'captado' WHERE phone = %s
    """
    cursor.execute(query, (phone,))
    connection.commit()
    cursor.close()
    connection.close()
