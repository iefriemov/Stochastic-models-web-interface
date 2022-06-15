import configparser
import psycopg2
import requests
import urllib


def get_interest():
    config = configparser.ConfigParser()
    config.read('./configurations_database.ini')
    config = config['PostgreSettings']
    conn = psycopg2.connect(
                            dbname=config['database'], 
                            user=config['user'], 
                            password=config['password'],
                            host=config['host']
                            )
    
    cursor = conn.cursor()
    cursor.execute('SELECT avg_interest_rate_amt FROM Treasury_Bills ORDER BY record_date ASC')
    records = cursor.fetchall()
    records = [el[-1] for el in records if el is not None]
    cursor.close()
    conn.close()
    return records

def run_dag():
    headers = {

    }

    json_data = {
        'conf': {},
    }

    response = requests.post('http://172.18.0.1:8080/api/v1/dags/Etl/dagRuns', headers=headers, json=json_data, auth=('airflow', 'airflow'))
