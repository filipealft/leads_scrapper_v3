import mysql.connector

def connect_to_database():
    conn = mysql.connector.connect(
        host='18.216.164.37',
        user='filipe_fortunato',
        password='Colorado13!',
        database='i9_tech',
        port='3306'
    )
    return conn

def send_daily_report():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = """
        select * from leads_raw
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)
    cursor.close()
    connection.close()


send_daily_report()