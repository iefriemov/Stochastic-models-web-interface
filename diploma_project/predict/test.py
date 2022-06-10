import configparser
import psycopg2

config = configparser.ConfigParser()
config.read('configurations_database.ini')
print(config['PostgreSettings']['database'])
conn = psycopg2.connect(
                        dbname=config['PostgreSettings']['database'], 
                        user=config['PostgreSettings']['user'], 
                        password=config['PostgreSettings']['password'],
                        host='172.18.0.1'
                        )
cursor = conn.cursor()
cursor.execute('SELECT avg_interest_rate_amt FROM Treasury_Bills ORDER BY record_date ASC')
records = cursor.fetchall()
print(records)
cursor.close()
conn.close()