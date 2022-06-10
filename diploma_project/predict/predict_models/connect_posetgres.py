import configparser
import psycopg2

def get_interest():
    config = configparser.ConfigParser()
    config.read('./configurations_database.ini')
    conn = psycopg2.connect(
                            dbname='airflow', 
                            user='airflow', 
                            password='airflow',
                            host='172.18.0.1'
                            )
    
    cursor = conn.cursor()
    cursor.execute('SELECT avg_interest_rate_amt FROM Treasury_Bills ORDER BY record_date ASC')
    records = cursor.fetchall()
    records = [el[-1] for el in records if el is not None]
    cursor.close()
    conn.close()
    return records